<template>
  <vue-cal 
      @cell-click="bookTimeSlot" 
      :events="appointments" 
      :time-step="60"
      :disabled-week-days=[0,6]  
      :time-from="9 * 60"          
      :time-to="17 * 60"
      :hide-weekends="true"
  />
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
  computed:{
    disabledDates() {
      const dates = [];
      // Generate dates for the next X days
      for (let d = new Date(); d < new Date(new Date().getTime() + 60 * 24 * 60 * 60 * 1000); d.setDate(d.getDate() + 1)) {
        if (d.getDay() === 0 || d.getDay() === 6) {
          // Format the date as 'YYYY-MM-DD'
          dates.push(d.toISOString().split('T')[0]);
        }
      }
      return dates;
    }
  },
  methods: {
    async bookTimeSlot(dateString) {
      let clickedDate = new Date(dateString);
      
      // Validation code...

      clickedDate.setMinutes(0, 0, 0);
      let endTime = new Date(clickedDate.getTime() + 60 * 60000);

      // Get the timezone offset in minutes and convert it to milliseconds
      let timezoneOffset = clickedDate.getTimezoneOffset() * 60000;

      // Adjust the dates to maintain the local time when converting to ISO string
      let localStartISO = new Date(clickedDate - timezoneOffset).toISOString().slice(0, -1);
      let localEndISO = new Date(endTime - timezoneOffset).toISOString().slice(0, -1);

      try {
        const userConfirmed = await this.promptForBookingDetails(clickedDate);
  
        if (userConfirmed) {
          const bookingDetails = {
            sDateTime: localStartISO,
            eDateTime: localEndISO,
            video: "", 
            cid: this.counselorId,
            sid: '65449c50032028ae33e59d15'
          };

          // Post the booking details to the server
          const response = await axios.post('https://smu-team06-api.ede20ab.kyma.ondemand.com/booking', bookingDetails);
          console.log('Server response:', response.data);
          
          if(response){
            console.log('response:', response.data._id);
            const jitsiMeetURL = `https://meet.jit.si/${encodeURIComponent('Telemed-Session-' + response.data._id)}`;
            const putComplete = await axios.put(`https://smu-team06-api.ede20ab.kyma.ondemand.com/booking/${response.data._id}`, {
              video: jitsiMeetURL
            });
            bookingDetails.video = jitsiMeetURL;
            if(putComplete){
              this.appointments.push({
              start: bookingDetails.sDateTime,
              end: bookingDetails.eDateTime,
              video: bookingDetails.video,
              title: 'New Appointment',
              class: 'bg-primary text-white'
              });
            }
            window.location.reload();
          }
        } else {
          console.log('Booking was not confirmed by the user.');
        }
      } catch (error) {
        console.error('An error occurred during booking:', error);
      }
    },
    getAppointmentbyCounselor(){
      axios.get(`https://smu-team06-api.ede20ab.kyma.ondemand.com/booking/${this.counselorId}`)
      .then(response => {
        this.appt = response.data;
        console.log('appt:', this.appt)
        this.populateAppointments();
        console.log('populateAppointments');
      })
      .catch(error => {
        console.error('Error fetching appointment data:', error);
        this.error = 'Failed to load the appointment data.'; // Set the error variable here
        this.loading = false;
      }); 

    },
    populateAppointments() {
      if (this.appt && Array.isArray(this.appt)) {
        this.appointments = this.appt.map(appt1 => ({
          title: '', // Replace with actual title if available
          start: new Date(appt1.sDateTime),
          end: new Date(appt1.eDateTime),
          class: 'bg-primary text-white',
        }));
      }
    },

    promptForBookingDetails(date) {
      return new Promise((resolve) => {
        const userConfirmed = confirm(`Confirm booking on ${date.toLocaleString()} for 1 hour?`);
        resolve(userConfirmed);
      });
    }
  }
};
</script>
