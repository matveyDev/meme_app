<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h3 mb-6">Create New Meme</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-form @submit.prevent="createMeme">
          <v-card>
            <v-card-text>
              <v-text-field
                v-model="meme.name"
                label="Meme Name"
                required
              ></v-text-field>

              <v-text-field
                v-model="meme.image"
                label="Image URL"
                required
              ></v-text-field>

              <v-select
                v-model="meme.spice_id"
                :items="spices"
                item-title="name"
                item-value="id"
                label="Select Spice"
                required
              ></v-select>

              <v-select
                v-model="meme.animal_slug_id"
                :items="animals"
                item-title="name"
                item-value="slug_id"
                label="Select Animal"
                required
              ></v-select>

              <v-text-field
                v-model="meme.points"
                label="Points"
                type="number"
                required
              ></v-text-field>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                type="submit"
                :loading="loading"
              >
                Create Meme
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateView',
  data() {
    return {
      meme: {
        name: '',
        image: '',
        spice_id: null,
        animal_slug_id: null,
        points: 0,
        user_id: '1' // TODO: Replace with actual user ID
      },
      spices: [],
      animals: [],
      loading: false
    }
  },
  async created() {
    try {
      const [spicesResponse, animalsResponse] = await Promise.all([
        axios.get('http://localhost:8000/api/spices/'),
        axios.get('http://localhost:8000/api/animals/')
      ])
      
      this.spices = spicesResponse.data
      this.animals = animalsResponse.data
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  },
  methods: {
    async createMeme() {
      this.loading = true
      try {
        await axios.post('http://localhost:8000/api/mixeds/', this.meme)
        this.$router.push('/')
      } catch (error) {
        console.error('Error creating meme:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 