const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface User {
  id: string;
  username: string;
  created_at: string;
}

export interface SimulationState {
  grid: any[][];
  bot: {
    x: number;
    y: number;
    direction: string;
    inventory: { wood: number; stone: number };
  };
  population: number;
}

export interface SaveState {
  id: string;
  user_id: string;
  grid_json: any;
  wood_count: number;
  stone_count: number;
  population_count: number;
  created_at: string;
  updated_at: string;
}

class ApiClient {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;

  setTokens(accessToken: string, refreshToken: string) {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  loadTokens() {
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_URL}${endpoint}`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  async register(username: string, password: string): Promise<User> {
    return this.request<User>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async login(username: string, password: string): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    this.setTokens(response.access_token, response.refresh_token);
    return response;
  }

  async refreshAccessToken(): Promise<AuthResponse> {
    if (!this.refreshToken) {
      throw new Error('No refresh token available');
    }
    const response = await this.request<AuthResponse>('/api/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: this.refreshToken }),
    });
    this.setTokens(response.access_token, response.refresh_token);
    return response;
  }

  async getSimulationState(): Promise<SimulationState> {
    return this.request<SimulationState>('/api/simulation/state');
  }

  async saveSimulationState(data: {
    grid_json: any;
    wood_count: number;
    stone_count: number;
    population_count: number;
  }): Promise<SaveState> {
    return this.request<SaveState>('/api/simulation/save', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getSavedState(): Promise<SaveState> {
    return this.request<SaveState>('/api/simulation/save');
  }
}

export const apiClient = new ApiClient();
apiClient.loadTokens();
