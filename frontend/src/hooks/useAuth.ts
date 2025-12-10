/**
 * Hook personalizado para autenticación
 */
import { useAuthContext } from '../context/AuthContext';

export const useAuth = () => {
  return useAuthContext();
};

export default useAuth;






