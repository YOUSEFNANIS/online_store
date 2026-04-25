import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useRoleStore = defineStore('role', () => {
  // Use 'const' instead of 'var' for modern JS standards
  const role = ref(localStorage.getItem('role') || null);
  
  function set_role(user_role) {
    // ALWAYS use .value to update a ref
    role.value = user_role
    localStorage.setItem('role', role.value)
    console.log(role.value)
  }
  function logout(){
    localStorage.removeItem('role')
    role.value = null
  }
  // Return the state and the action so components can use them
  return { role, set_role, logout }
})