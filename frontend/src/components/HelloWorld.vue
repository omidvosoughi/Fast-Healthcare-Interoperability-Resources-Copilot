<template>
  <div>
    <h1>Create StructureDefinition</h1>
    <textarea v-model="structureDefinitionJson" rows="10" cols="50"></textarea>
    <button class="btn btn-primary" @click="submitDefinition">Submit</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      // Initialize structureDefinitionJson as an object, then stringify
      structureDefinitionJson: JSON.stringify({
        "resourceType": "StructureDefinition",
        "url": "http://fhir.kids-first.io/StructureDefinition/Patient",
        "version": "0.1.0",
        "name": "kids_first_research_participant",
        "title": "Kids First Research Participant",
        "status": "draft",
        "publisher": "Kids First DRC",
        "description": "The individual human or other organism.",
        "fhirVersion": "4.0.0",
        "kind": "resource",
        "abstract": false,
        "type": "Patient",
        "baseDefinition": "http://hl7.org/fhir/StructureDefinition/Patient",
        "derivation": "constraint",
        "differential": {
            "element": [
                {
                    "id": "Patient",
                    "path": "Patient"
                },
                {
                    "id": "Patient.identifier",
                    "path": "Patient.identifier",
                    "mustSupport": true
                },
                {
                    "id": "Patient.name",
                    "path": "Patient.name",
                    "max": "0"
                },
                {
                    "id": "Patient.telecom",
                    "path": "Patient.telecom",
                    "max": "0"
                },
                {
                    "id": "Patient.address",
                    "path": "Patient.address",
                    "max": "0"
                },
                {
                    "id": "Patient.photo",
                    "path": "Patient.photo",
                    "max": "0"
                },
                {
                    "id": "Patient.contact",
                    "path": "Patient.contact",
                    "max": "0"
                },
                {
                    "id": "Patient.gender",
                    "path": "Patient.gender",
                    "min": 1
                }
            ]
        }
      }, null, 2) // Pretty print JSON
    };
  },
  methods: {
    submitDefinition() {
      // Parse the JSON string to an object to send as JSON body
      const structureDefinition = JSON.parse(this.structureDefinitionJson);
      axios.post('http://localhost:8000/create-structure-definition/', structureDefinition)
        .then(response => alert('Success: ' + JSON.stringify(response.data)))
        .catch(error => console.error('Error: ' + error));
      
        // // Validate the StructureDefinition
        // axios.post("http://localhost:8000/StructureDefinition/$validate", structureDefinition)
        //   .then(responseValidate => alert('Validate Successed.' + responseValidate))
        //   .catch(errorValidate => alert('Error:' + errorValidate));

        // Check the response

        // if response_validate.status_code == 200:
        //     print("Validation successful!")
        //     print(response.json()) 
        // else:
        //     print("Validation failed.")
        //     print(response.text)
    }
  }
}
</script>
