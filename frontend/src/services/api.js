import axios from 'axios'
import i18n from '@/i18n'

export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const t = (key) => i18n.global.t(key)

const api = axios.create({
  baseURL: API_URL + '/',
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

api.interceptors.request.use((config) => {
  config.headers['Accept-Language'] = i18n.global.locale.value;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/api/token/')
    ) {
      originalRequest._retry = true;

      try {
        await api.post('/api/token/refresh/');
        return api(originalRequest);
      } catch (err) {
        return Promise.reject(err);
      }
    }

    // Pages that render their own errors set `skipGlobalError` in the request config.
    // Auth/signup forms handle theirs inline.
    const url = originalRequest?.url || '';
    const handledInline = originalRequest?.skipGlobalError || url.includes('/api/token/') || url.includes('/signup/');
    // 401s are silent: anonymous visitors hit them on normal page loads.
    if (!handledInline && error.response?.status !== 401) {
      let message;
      if (!error.response) message = t('errors.network');
      else if (error.response.status === 403) message = t('errors.forbidden');
      else if (error.response.status === 404) message = t('errors.notFound');
      else if (error.response.status >= 500) message = t('errors.server');
      else message = error.response.data?.detail || t('errors.generic');
      window.dispatchEvent(new CustomEvent('api-error', { detail: message }));
    }

    return Promise.reject(error);
  }
);


export default api;