import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import { api } from './api';

vi.mock('./api', () => ({
  api: vi.fn(),
  clearSession: vi.fn(),
  getToken: vi.fn(() => 'test-token'),
  getUser: vi.fn(() => ({ name: 'Test User', role: 'user' })),
}));

const vehicles = [
  { id: 1, make: 'Toyota', model: 'Corolla', category: 'Sedan', price: 24000, quantity: 2 },
  { id: 2, make: 'Honda', model: 'Civic', category: 'Sedan', price: 28000, quantity: 0 },
];

describe('inventory dashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    api.mockResolvedValue(vehicles);
  });

  it('filters vehicles by make, model, and category text', async () => {
    render(<App />);
    await screen.findByText('Toyota');

    fireEvent.change(screen.getByLabelText('Search vehicles'), { target: { value: 'honda' } });

    expect(screen.queryByText('Toyota')).not.toBeInTheDocument();
    expect(screen.getByText('Honda')).toBeInTheDocument();
  });

  it('disables purchase when a vehicle has no stock', async () => {
    render(<App />);
    await screen.findByText('Honda');

    expect(screen.getByRole('button', { name: 'Unavailable' })).toBeDisabled();
  });

  it('refreshes stock after a successful purchase', async () => {
    api
      .mockResolvedValueOnce(vehicles)
      .mockResolvedValueOnce({ message: 'Purchase recorded' })
      .mockResolvedValueOnce([{ ...vehicles[0], quantity: 1 }, vehicles[1]]);

    render(<App />);
    await screen.findByText('Toyota');
    fireEvent.click(screen.getByRole('button', { name: 'Purchase' }));

    await waitFor(() => expect(screen.getByText('1 in stock')).toBeInTheDocument());
    expect(api).toHaveBeenCalledWith('/api/vehicles/1/purchase', { method: 'POST' });
  });
});
