<template>
<v-card class="mx-auto" md=5 max-width="600">
  <v-card-title>SignUp Form</v-card-title>

  <v-form v-model="valid">
    <v-text-field v-model="userInfo.username" 
                  label="Name" 
                  color="green"
                  :rules="[required('name')]"
                  class="input-group--focused"
                  v-if="hasName" />

    <v-text-field v-model="userInfo.email" 
                  label="Email"
                  color="green" 
                  :rules="[required('email'), emailFormat()]"/>

    <UserAuthPassword v-model="userInfo.password" label="Password" />

    <div v-if="signUpCheckboxes">
      <!-- v-model connects it with the userInfo hash, value makes the :rules work -->
      <v-checkbox v-model="userInfo.agreeToTerms"
                  value="userInfo.agreeToTerms"
                  class="mr-0"
                  color="green"
                  :rules="[required('agreeToTerms', 'You must agree to the terms and conditions and privacy policy')]">
        <template #label>
          <span>
            I have read and agree to the 
            <a href="/policies/terms-and-conditions" target="_blank" @click.stop>Terms and Conditions</a>
            and 
            <a href="/policies/privacy-policy" target="_blank" @click.stop>Privacy Policy</a>
          </span>
        </template>
      </v-checkbox>

      <v-checkbox v-model="userInfo.email_weekly"
                  color="green"
                  label="I would like to join the VIP list and get a weekly newsletter." />
      <v-checkbox v-model="userInfo.email_daily"
                  color="green"
                  label="I would like to get an email notification whenever new videos or courses are released." />
    </div>

    <v-btn @click="submitForm(userInfo)" :disabled="!valid" color="green accent-3">{{ buttonText }}</v-btn>
  </v-form>
</v-card>
</template>

<script>
  import validations from "@/utils/validations";
  import UserAuthPassword from '@/components/UserAuthPassword.vue';

  export default {
    data() {
      return {
        valid: false,
        userInfo: {
          username: 'InHwan Jung',
          email: 'inhwan.jung@gmail.com',
          password: 'passw@rd',
          agreeToTerms: false,
          email_daily: true,
          email_weekly: true
        },
        ...validations
      }
    },
    components: {
      UserAuthPassword
    },
    props: {
      submitForm: {
        type: Function,
        required: true,
      },
      buttonText: {
        type: String,
        required: true,
      },
      hasName: Boolean,
      signUpCheckboxes: Boolean
    }
  }
</script>

<style lang="scss" scoped>

</style>