from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, select, update
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models import Purchase, User, Vehicle
from app.schemas import PurchaseOut, RestockRequest, VehicleCreate, VehicleOut, VehicleUpdate

router = APIRouter(prefix="/api/vehicles", tags=["Vehicles"])

@router.get("", response_model=list[VehicleOut])
def list_vehicles(available_only: bool = Query(False), db: Session = Depends(get_db)):
    stmt = select(Vehicle).order_by(Vehicle.id.desc())
    if available_only:
        stmt = stmt.where(Vehicle.quantity > 0)
    return list(db.scalars(stmt).all())

@router.get("/search", response_model=list[VehicleOut])
def search_vehicles(make: str | None = None, model: str | None = None, category: str | None = None, min_price: float | None = Query(None, ge=0), max_price: float | None = Query(None, ge=0), db: Session = Depends(get_db)):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=422, detail="min_price cannot be greater than max_price")
    stmt = select(Vehicle)
    if make and make.strip(): stmt = stmt.where(func.lower(Vehicle.make).contains(make.strip().lower()))
    if model and model.strip(): stmt = stmt.where(func.lower(Vehicle.model).contains(model.strip().lower()))
    if category and category.strip(): stmt = stmt.where(func.lower(Vehicle.category) == category.strip().lower())
    if min_price is not None: stmt = stmt.where(Vehicle.price >= min_price)
    if max_price is not None: stmt = stmt.where(Vehicle.price <= max_price)
    return list(db.scalars(stmt.order_by(Vehicle.id.desc())).all())

@router.post("", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
def create_vehicle(payload: VehicleCreate, db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle); db.commit(); db.refresh(vehicle)
    return vehicle

@router.put("/{vehicle_id}", response_model=VehicleOut)
def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: Session = Depends(get_db), _user: User = Depends(get_current_user)):
    vehicle = db.get(Vehicle, vehicle_id)
    if not vehicle: raise HTTPException(status_code=404, detail="Vehicle not found")
    changes = payload.model_dump(exclude_unset=True)
    for key, value in changes.items():
        if isinstance(value, str) and key in {"make", "model", "category"}: value = value.strip()
        setattr(vehicle, key, value)
    db.commit(); db.refresh(vehicle)
    return vehicle

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    vehicle = db.get(Vehicle, vehicle_id)
    if not vehicle: raise HTTPException(status_code=404, detail="Vehicle not found")
    if db.scalar(select(Purchase.id).where(Purchase.vehicle_id == vehicle_id).limit(1)):
        raise HTTPException(status_code=409, detail="Cannot delete a vehicle with purchase history")
    db.delete(vehicle); db.commit()

@router.post("/{vehicle_id}/purchase", response_model=PurchaseOut, status_code=status.HTTP_201_CREATED)
def purchase_vehicle(vehicle_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Atomic conditional update prevents two requests buying the last unit.
    result = db.execute(update(Vehicle).where(Vehicle.id == vehicle_id, Vehicle.quantity > 0).values(quantity=Vehicle.quantity - 1))
    if result.rowcount == 0:
        db.rollback()
        if not db.get(Vehicle, vehicle_id): raise HTTPException(status_code=404, detail="Vehicle not found")
        raise HTTPException(status_code=409, detail="Vehicle is out of stock")
    vehicle = db.get(Vehicle, vehicle_id)
    purchase = Purchase(user_id=user.id, vehicle_id=vehicle_id, quantity=1, unit_price=vehicle.price)
    db.add(purchase); db.commit(); db.refresh(purchase); db.refresh(vehicle)
    return {"message": "Purchase recorded successfully", "vehicle": vehicle, "purchase_id": purchase.id}

@router.post("/{vehicle_id}/restock", response_model=VehicleOut)
def restock_vehicle(vehicle_id: int, payload: RestockRequest, db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    result = db.execute(update(Vehicle).where(Vehicle.id == vehicle_id).values(quantity=Vehicle.quantity + payload.quantity))
    if result.rowcount == 0: raise HTTPException(status_code=404, detail="Vehicle not found")
    db.commit()
    return db.get(Vehicle, vehicle_id)
