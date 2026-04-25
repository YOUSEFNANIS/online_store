<template>
      <div class="main">
        <h1 class="page-title">Add product</h1>
        <!-- TITLE -->
        <div class="card">
          <label class="label">Title</label>
          <input v-model="product.name" class="input"/>
        </div>

        <!-- DESCRIPTION -->
        <div class="card">
          <label class="label">Description</label>
          <textarea v-model="product.description" class="textarea"></textarea>
        </div>

        <!-- MEDIA -->
        <div class="card">
          <label class="label">Media</label>

          <div class="media-upload">
            <input type="file" @change="uploadImage">
          </div>

          <div class="images">
            <li v-for="(img, index) in imagePreviews"  :key="index">
              <div class="image-item">
                  <img :src="img"/>
                  <button class="remove-btn" @click="removeElement(index)">x</button>
              </div>
                
            </li>
          </div>
        </div>

        <!-- PRICING -->
        <div class="card">

            <div class="row">
            <div  class="field">
              <label class="label">Price</label>
              <input type="number" v-model="product.price" class="input"/>
            </div>
            <div  class="field">
                <label class="label">Quantity</label>
                <input type="number" v-model="product.inventory" class="input"/>
          </div>
          </div>
          <button class="save-btn" @click="saveProduct">
          Save product
        </button>
        </div>
      </div>
</template>

<script>

import api from '@/services/api';


export default {
  
  data() {
    return {
      product: {
        name: "",
        description: "",
        price: null,
        inventory: 0,
        },
        imagesfile: [],
        imagePreviews: [],
        product_id: null,
    }
  },
  
  methods: {

    uploadImage(e) {
      const file = e.target.files[0]
      const url = URL.createObjectURL(file)

      if (!file) return

      this.imagesfile.push(file)
      this.imagePreviews.push(url);
    },

    removeElement(e){
      this.imagePreviews.splice(e, 1)
    },

    async saveProduct() {

              try{
                const response = await api.post('/core/products/', this.product)
                      this.product_id = response.data.id
                  }
              catch(error){
                    console.log(error.response)
                  }
              try {
                const formData = new FormData()

                for (let file of this.imagesfile){
                  formData.append("image", file)
                  formData.append("product", this.product_id)
                }
                const url = '/core/products/' + this.product_id + '/images/';
                    const response = await api.post(url,  formData,{headers: 
                        {
                          "Content-Type": "multipart/form-data"
                        }})
                this.$emit('saved', true);
                    }
              catch(error){
                      console.log(error.response)
              }

              
    }
    
  }
}
</script>

<style scoped>

.main{
  flex:3;
  font-size: large;
  display: flex;
  margin-top: 5%;
  flex-direction: column;
  align-items: center;
}

.sidebar{
  flex:1;
}

.card{
  background:white;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60%;
  padding:20px;
  border-radius:8px;
  margin-bottom:20px;
  box-shadow:0 1px 2px rgba(0,0,0,0.05);
}

.label{
  font-weight:600;
  display:block;
  margin-bottom:6px;
}

.input{
  width:90%;
  padding:10px;
  border:2px solid #919090;
  border-radius:6px;
  margin-bottom:12px;
}

.textarea{
  width:90%;
  height:120px;
  border:2px solid #919090;
  border-radius:6px;
  padding:10px;
}

.section-title{
  margin-bottom:10px;
}

.row{
  display:flex;
  width: 60%;
  justify-content: space-between;
  align-items: flex-start;
  padding: 23px;
  gap:10px;
}

.row input{
  width: 100%;
  box-sizing: border-box;
}

.media-upload{
  border:2px dashed #919090;
  width: 90%;
  padding:20px;
  text-align:center;
}

.images{
  display:flex;
  flex-wrap:wrap;
   gap:25px;
  margin-top:10px;
}

.images img{
  width:30% + 6px;
  height:30% + 6px;
  padding: 10px;
  max-width: 300px;
  max-height:300px;
  border-radius: 4px;
  border: 3px solid #000000;   /* 4px is "thick", solid style, using existing light gray */
  box-sizing: border-box;
}

.save-btn{
  width:60%;
  padding:12px;
  background:#000000;
  color:white;
  border:none;
  border-radius:6px;
  font-weight:bold;
  cursor:pointer;
}

.save-btn:hover{
  background:#1e1e1e;
}

.image-item{
  position: relative;
  display: inline-block;
}

.remove-btn{
  position: absolute;
  top: 6px;
  right: 6px;

  width: 26px;
  height: 26px;

  border: none;
  border-radius: 50%;

  background: #ff4d4f;
  color: white;

  font-size: 16px;
  font-weight: bold;
  line-height: 26px;

  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn:hover{
  background: #d9363e;
  transform: scale(1.1);
}


</style>