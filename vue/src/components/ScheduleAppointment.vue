<template>
    <vue-cal @cell-click="bookTimeSlot" :events="appointments" />
  </template>
  
  <script>
  import VueCal from 'vue-cal';
  import 'vue-cal/dist/vuecal.css';
  import axios from 'axios';
  
  export default {
    components: { VueCal },
    props: {
      counselorId: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        appointments: [
            // Example event structure
            { start: new Date(2023, 11, 15, 10), end: new Date(2023, 11, 15, 11), title: 'Existing Appointment' },
            // More events...
        ],
        appt: []
      };
    },
    created() {
        if(this.counselorId){
            this.getAppointmentbyCounselor();
        }
    },
    methods: {
      async bookTimeSlot({ date }) {
        // Assuming you have a modal or form to fill out the booking
        const bookingDetails = await this.promptForBookingDetails(date);
        
        // Send bookingDetails to your backend
        try {
          const response = await axios.post('/api/bookings', bookingDetails);
          // Handle successful booking, e.g., add to appointments
          this.appointments.push(response.data);
        } catch (error) {
          // Handle errors, e.g., notify user of the failed booking
          console.error('Failed to book appointment:', error);
        }
      },
      getAppointmentbyCounselor(){
        axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/booking/${this.counselorId}`)
        .then(response => {
          this.appt = response.data;
          console.log('Appointment:', this.appt)
        })
        .catch(error => {
          console.error('Error fetching appointment data:', error);
          this.error = 'Failed to load the appointment data.'; // Set the error variable here
          this.loading = false;
        }); 

      },
      promptForBookingDetails(date) {
        // Logic to ask the user for booking details (e.g., open a modal)
        // Return booking details as an object
        return new Promise((resolve) => {
          // Mock-up prompt logic
          resolve({
            date: date,
            title: 'New Appointment',
            // ... other booking details
          });
        });
      }
    }
  };
  </script>
  