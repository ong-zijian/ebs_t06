<template>
    <vue-cal @cell-click="bookTimeSlot" :events="appointments" />
    <button @click="checkAppointment()">Check</button>
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
      appointments: [],
      appt: null,
    };
  },
  created() {
      if(this.counselorId){
          this.getAppointmentbyCounselor();
      }
  },
  methods: {
    checkAppointment(){
      console.log(this.appointments);
    },
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
        console.log('appt:', this.appt)
        this.populateAppointments();
      })
      .catch(error => {
        console.error('Error fetching appointment data:', error);
        this.error = 'Failed to load the appointment data.'; // Set the error variable here
        this.loading = false;
      }); 

    },
    populateAppointments() {
      if (this.appt && Array.isArray(this.appt)) {
        // Clear the current appointments to ensure reactivity
        this.appointments = [];

        // Populate the appointments with new data
        const updatedAppointments = this.appt.map(appt => {
          // Parse the dates with the correct timezone offset if needed
          const start = new Date(appt.sDateTime);
          const end = new Date(appt.eDateTime);

          // Check if the dates are valid before returning the event object
          if (!isNaN(start.getTime()) && !isNaN(end.getTime())) {
            return {
              start: start,
              end: end,
              title: `Session with counselor ${appt.cid}`,
            };
          }
          return null;
        }).filter(event => event); // Filter out null values

        // Use Vue's $set to ensure the appointments are reactive
        this.$set(this, 'appointments', updatedAppointments);
      }
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
