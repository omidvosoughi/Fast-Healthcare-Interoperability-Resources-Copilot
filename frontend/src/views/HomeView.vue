<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <fhirToolkit msg="Fast Healthcare Interoperability Resources (FHIR) Toolkit"/>
  </div>
</template>

<script>
// @ is an alias to /src
import fhirToolkit from '@/components/fhirToolkit.vue'

export default {
  name: 'HomeView',
  components: {
    fhirToolkit
  }
}
</script>
