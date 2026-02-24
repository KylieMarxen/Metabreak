// js/api-client.js
// API client for MetaBreak backend integration

const API_BASE_URL = 'http://localhost:5000/api';

class MetaBreakAPI {
  constructor() {
    this.token = localStorage.getItem('mb_auth_token');
  }

  // Helper method to make authenticated requests
  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // ==================== AUTH METHODS ====================

  async register(username, email, password) {
    const data = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password })
    });
    
    this.token = data.access_token;
    localStorage.setItem('mb_auth_token', this.token);
    localStorage.setItem('mb_current_user', JSON.stringify(data.user));
    
    return data;
  }

  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    
    this.token = data.access_token;
    localStorage.setItem('mb_auth_token', this.token);
    localStorage.setItem('mb_current_user', JSON.stringify(data.user));
    
    return data;
  }

  logout() {
    this.token = null;
    localStorage.removeItem('mb_auth_token');
    localStorage.removeItem('mb_current_user');
  }

  async getCurrentUser() {
    return await this.request('/auth/me');
  }

  isAuthenticated() {
    return !!this.token;
  }

  getCurrentUserFromStorage() {
    const userStr = localStorage.getItem('mb_current_user');
    return userStr ? JSON.parse(userStr) : null;
  }

  // ==================== GAME METHODS ====================

  async getAllGames() {
    return await this.request('/games');
  }

  async searchGames(query) {
    return await this.request(`/games/search?q=${encodeURIComponent(query)}`);
  }

  async getGame(gameId) {
    return await this.request(`/games/${gameId}`);
  }

  // ==================== REVIEW METHODS ====================

  async getReviews(options = {}) {
    const params = new URLSearchParams();
    
    if (options.page) params.append('page', options.page);
    if (options.per_page) params.append('per_page', options.per_page);
    if (options.sort) params.append('sort', options.sort);
    if (options.game_id) params.append('game_id', options.game_id);
    
    const queryString = params.toString();
    const endpoint = queryString ? `/reviews?${queryString}` : '/reviews';
    
    return await this.request(endpoint);
  }

  async getReview(reviewId) {
    return await this.request(`/reviews/${reviewId}`);
  }

  async createReview(reviewData) {
    return await this.request('/reviews', {
      method: 'POST',
      body: JSON.stringify(reviewData)
    });
  }

  async updateReview(reviewId, reviewData) {
    return await this.request(`/reviews/${reviewId}`, {
      method: 'PUT',
      body: JSON.stringify(reviewData)
    });
  }

  async deleteReview(reviewId) {
    return await this.request(`/reviews/${reviewId}`, {
      method: 'DELETE'
    });
  }

  // ==================== VOTE METHODS ====================

  async voteReview(reviewId, voteType) {
    return await this.request(`/reviews/${reviewId}/vote`, {
      method: 'POST',
      body: JSON.stringify({ vote_type: voteType })
    });
  }

  // ==================== COMMENT METHODS ====================

  async getComments(reviewId) {
    return await this.request(`/reviews/${reviewId}/comments`);
  }

  async createComment(reviewId, content) {
    return await this.request(`/reviews/${reviewId}/comments`, {
      method: 'POST',
      body: JSON.stringify({ content })
    });
  }

  async deleteComment(commentId) {
    return await this.request(`/comments/${commentId}`, {
      method: 'DELETE'
    });
  }

  // ==================== FILE UPLOAD ====================

  async uploadCover(file) {
    const formData = new FormData();
    formData.append('file', file);

    const headers = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}/upload/cover`, {
      method: 'POST',
      headers,
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Upload failed');
    }

    return await response.json();
  }

  // ==================== ANALYTICS ====================

  async getDashboardStats() {
    return await this.request('/stats/dashboard');
  }

  // ==================== HEALTH CHECK ====================

  async healthCheck() {
    return await this.request('/health');
  }
}

// Create global API instance
window.API = new MetaBreakAPI();

// Helper function to show notifications
window.showNotification = function(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 1rem 1.5rem;
    background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#00ffc6' : '#5be3ff'};
    color: ${type === 'success' ? '#070b16' : '#ffffff'};
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 10000;
    animation: slideIn 0.3s ease;
    font-weight: 600;
  `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
};

// Add CSS for notifications
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(400px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(400px); opacity: 0; }
  }
`;
document.head.appendChild(style);