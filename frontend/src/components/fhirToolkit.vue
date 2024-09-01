<template>
    <div class="row header">
        <div class="col-12">
            <h1>Fast Healthcare Interoperability Resources (FHIR) Copilot</h1>
        </div>
    </div>
    
    <div class="row content">
        <div class="col-6">
          <div class="alert alert-primary" role="alert">
            {{ contentTitle }}
          </div>
          <div class="row">
            <div class="chat-section">
              <ChatComponent @bot-reply="handleBotReply" />
            </div>
          </div>
          
          
        </div>
        <div class="col-6">
          <div class="alert alert-success" role="alert">
            Response:
          </div>
          
          <div class="row">
            <div class="chat-window" ref="chatWindow">
              <div v-for="(message, index) in messages" :key="index" class="chat-message" :class="message.type">
                <div class="message-content">
                  <pre>{{ message.content }}</pre>
                </div>
              </div>
            </div>
          </div>
          
          <div class="row">
            <div class="col-6">
              <button class="btn btn-success submit-btn" @click="mapEntitiesToSNOMED" :disabled="isSnomedButtonDisabled">
                <span v-if="loading_1" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>2. Map entities to SNOMED CT</span>
              </button>
            </div>
            <div class="col-6">
              <button class="btn btn-success submit-btn" @click="validateEntitiesWithSNOMED" :disabled="isValidateButtonDisabled">
                <span v-if="loading_2" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span v-else>3. Match and validate entities with SNOMED CT</span>
              </button>
            </div>
          </div>
          
        </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import ChatComponent from './ChatComponent.vue';
  
  
  export default {
    name: 'FhirToolkit',
    components: {
      ChatComponent
    },
    data() {
      return {
        // Initialize structureDefinitionJson as an object, then stringify
        message:null,
        response_active : false,
        loading_1: false,
        loading_2: false,
        // contentTitle: 'Define a Prompt:',
        contentTitle: 'Define a Prompt:',
        responseTitle: 'Response: ',
        PR_disabled: true,
        att_disabled: true,
        search_disabled: true,
        botResponse: '',
        mappedEntities: {},  // New state to store mapped entities
        validatedEntities: {},
        formattedDict: '',
        messages: [],
        // mapped_response: null,
      };
    },
    mounted() {
      this.formattedDict = this.formatDict(this.validatedEntities);
    },
    computed: {
      isSnomedButtonDisabled() {
        // return this.botResponse.trim() === '';
        return !this.messages.some(msg => msg.type === 'bot');
      },
      isValidateButtonDisabled() {
        // The "Match and validate entities with SNOMED CT" button should be enabled only if there are mapped entities
        return Object.keys(this.mappedEntities).length === 0;
      },
      hasMappedEntities() {
        return Object.keys(this.mappedEntities).length > 0;
      }
    },
    watch: {
      messages() {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    methods: {
      formatDict(dict) {
        return JSON.stringify(dict, null, 2);
      },
      scrollToBottom() {
        const chatWindow = this.$refs.chatWindow;
        if (chatWindow) {
          chatWindow.scrollTop = chatWindow.scrollHeight;
        }
      },
      handleBotReply(response) {
        // this.botResponse += JSON.stringify(response, null, 2);
        this.messages.push({
          type: 'bot',
          content: JSON.stringify(response, null, 2)
        });
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      async mapEntitiesToSNOMED() {
        try {
          this.loading_1 = true;
          const response = await axios.post('http://localhost:8000/map-entities', {
            // text: this.botResponse
            text: this.messages.find(msg => msg.type === 'bot').content
          });
          this.message = "Entities successfully mapped to SNOMED CT.";
          this.response_active = true;
        
        // Store the mapped entities
          this.mappedEntities = response.data.mapped_entities || {};
          // this.botResponse += '\n\n **Entities successfully mapped to SNOMED CT** \n\n ' + this.mappedEntities;
          this.messages.push({
            type: 'info',
            content: '**Entities successfully mapped to SNOMED CT** \n\n' + JSON.stringify(this.mappedEntities, null, 2)
          });
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        } catch (error) {
          // this.message = 'Error: ' + error.response.data.message;
          // console.error(error);
          this.messages.push({
            type: 'error',
            content: 'Error: ' + error.response.data.message
          });
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        } finally {
          this.loading_1 = false;
        }
      },
      async validateEntitiesWithSNOMED() {
        try {
          this.loading_2 = true;
          const response = await axios.post('http://localhost:8000/validate-entities', {
            entities: JSON.stringify(this.mappedEntities, null, 2)
          });
          this.message = "Entities successfully validated with SNOMED CT.";
          this.response_active = true;

          this.validatedEntities = response.data.validation_results || {};
          
          this.messages.push({
            type: 'info',
            content: '**Entities validated with SNOMED CT using similarity scores calculated via the cosine similarity function** \n\n' + JSON.stringify(this.validatedEntities, null, 2)
          });
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        } catch (error) {
          // this.message = 'Error: ' + (error.response ? error.response.data.message : error.message);
          // console.error(error);
          this.messages.push({
            type: 'error',
            content: 'Error: ' + (error.response ? error.response.data.message : error.message)
          });
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        } finally {
          this.loading_2 = false;
        }
      },
      
    }
  }
  </script>

  <style>
  .header{
    margin: 25px;
  }
  .header h1{
    color: white;
    margin-top: 10px;
  }
  .menu{
    margin: 25px;
  }
  .menu button{
    padding: 20px;
    width: 300px;
    height: 100px;
  }
  /* .content textarea{
    width: 90%;
    height: 620px;
    margin: 20px;
  } */
  .content .submit-btn{
    width: 300px;
    height: 80px;
  }
  .alert {
    margin: 20px;
  }
  .alert_response {
    margin: 40px;
    display: none;
  }
  .alert_response_show {
    display: inherit;
  }
  .btn-menu {
    margin: 10px;
  }
  .chat-section {
    width: 92% !important;
    height: 500px;
    margin: 20px;
    /* Add any additional styles you need for the chat section */
  }
  .bot-response {
    margin-top: 20px;
    color: white;
  }
  .chat-window {
    width: 92%;
    height: 550px;
    overflow-y: auto;
    padding: 20px;
    /* background-color: #f7f7f7; */
    border: 1px solid #ddd;
    margin: 36px;
    border-radius: 10px;
  }
  .chat-message {
    margin: 10px 0;
    padding: 10px;
    border-radius: 10px;
    max-width: 100%;
    word-wrap: break-word;
  }
  .chat-message.bot {
    background-color: #d1e7dd;
    text-align: left;
  }

  .chat-message.info {
    background-color: #cff4fc;
    text-align: left;
  }

  .chat-message.error {
    background-color: #f8d7da;
    text-align: left;
  }

  .chat-message .message-content {
    white-space: pre-wrap;
  }

</style>
  