<template>
  <div class="container">

    <div class="order-id-header">
      <h2>#order Id: {{ $route.params.orderId }}</h2>
      <h2>{{ customer_name }}</h2>
    </div>
    <div class="form-row">
        <input 
            type="text" 
            v-model="location" 
            class="laction-field"
            placeholder="location"
        >

        <div class="price-row">
        <input 
            type="text" 
            placeholder="total price"
            v-model="price" 
            class="price-input"
        >
        
        <span>LYD</span>
    </div>
    </div>

    

    <div class="actions">
        <button @click="save" class="btn">save</button>
        <button @click="handleCancel" class="btn">cancel</button>
    </div>
  </div>
</template>
<script>
import api from '@/services/api';


    export default{
      mounted(){
        this.retreiveItems()
      },
        data() {
            return {
              id: this.$route.params.orderId,
              orderTemp: {},
              location: '',
              price: null,
              customer_name: null,
            }
        },
        methods: {
            async save() {
                try {
                  // 3. Send the PUT request to your backend
                  // Assuming your API expects: http://127.0.0.1:8000/orders/{id}/
                const response = await api.patch(`http://127.0.0.1:8000/core/orders/${this.id}/`, {'location': this.location, 'total_value': this.price});

                  // 4. (Optional) Redirect the user back to the list or details page
                this.$router.push('/orderslist'); 
                this.$emit('saved', true)

        } catch (error) {
            console.error("Error saving data:", error);
            alert('Failed to save data. Please try again.');
        }
            },
            handleCancel() {
                // Logic for resetting or closing goes here
            },
            
        }
    }

</script>

<style scoped>
        
         .container {
          position: absolute;
          top: 30%;
          left: 30%;
          background: white;
          border: 1px solid #ebebeb;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
          overflow: hidden;
          padding: 2.5rem;
          max-width: 700px
        }
.order-id-header {
    width: 100%;
    display: flex;
    background-color: #fcfcfc;
    justify-content: space-between;
    border-bottom: 2px solid #000000; /* That specific blue line from your image */
    margin-bottom: 2rem;
}

.order-id-header h2 {
    margin: 0;
    padding: 0px 0px 20px 0px;
    font-size: 1.2rem;
    font-weight: 500;
    color: #111;
    /* This makes it look like the "typewriter" or clean font in your pic */
}
.form-row {
    display: flex;
    width: 100%; /* Changed from fit-content */
    align-items: flex-end;
    justify-content: space-between; 
    border: 20px 0px;
    gap: 2rem;
    margin-bottom: 2.5rem;
}

.laction-field {
    flex: 2;
}

.price-row {
    display: flex;
    width: fit-content;
    align-items: flex-end;
    gap: 1rem;
    flex: 1; /* Takes up less space */
}

.actions {
    display: flex;
    flex: 1;
    gap: 1rem;
    margin-top: 1rem;
}

input {
    flex: 1;
    border: none;
    border-bottom: 1.5px solid #999;
    background: transparent;
    font-size: 1.2rem;
    outline: none;
    transition: border-color 0.2s;
}

input:focus {
    border-bottom-color: #3b82f6;
}
</style>
