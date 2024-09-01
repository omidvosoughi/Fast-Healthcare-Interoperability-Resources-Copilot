<template>
  <div class="row">
    <div class="col-6">
      <div class="chat-container-prompt">
        
        <div class="alert alert-secondary" role="alert">
          Please identify FHIR resource types: 
        </div>

        <!-- Checkboxes for inserting text -->
        <div class="row">
          <div class="col-12">
            <div class="checkbox-container d-flex flex-wrap">
              <label v-for="(content, key) in checkboxTexts" :key="key" class="checkbox-label">
                <input type="checkbox" v-model="selectedCheckboxes" :value="key" @change="updateTextareaWithCheckboxes" />
                {{ key }}
              </label>
            </div>
          </div>
          
        </div>
        
        <textarea v-model="promptText" class="promptText" ref="promptTextarea"></textarea>
        
      </div>
    </div>
    <div class="col-6">
      <div class="chat-container">
        <div class="messages" ref="messagesContainer">
          <div v-for="message in messages" :key="message.id" :class="['message', message.sender]">
            {{ message.text }}
          </div>
        </div>
          
        <div class="input-container">
          <textarea v-model="newMessage" @keyup.enter="sendMessage" placeholder="Insert your clinical note..." class="message-input"></textarea>
          <button class="btn btn-primary send-button" @click="sendMessage" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            <span v-if="!loading">1. Extract clinical entities</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatComponent',
  data() {
    return {
      messages: [],
      newMessage: '',
      content: '',
      extractorData: {
        name: '',
        text: ''
      }, 
      selectedPrompt: 'extract',
      prompts: [],
      promptText: '',
      promptText_send: '',
      checkboxTexts: {
        'Encounter': "An encounter is a recorded interaction between a patient and healthcare provider for delivering healthcare services or assessing the patient's health, while an appointment documents planned activities.",
        'Condition': 'A clinical condition, problem, diagnosis, or other event, situation, issue, or clinical concept that has risen to a level of concern.',
        'Procedure': 'An action performed on or for a patient, practitioner, device, organization, or location, ranging from medical interventions to inspections, counseling, or accreditation procedures.',
        'Medication': 'This resource is primarily used for the identification and definition of a medication, including ingredients, for the purposes of prescribing, dispensing, and administering a medication as well as for making statements about medication use.',
        'MedicationStatement': 'Record of medication being taken by a patient.',
        'MedicationAdministration': 'Describes the event of a patient consuming or otherwise being administered a medication. This may be as simple as swallowing a tablet or it may be a long running infusion. Related resources tie this event to the authorizing prescription, and the specific encounter between patient and health care practitioner.',
        'Observation': 'Measurements and simple assertions made about a patient, device or other subject.',
        'DiagnosticReport': 'A combination of request information, atomic results, images, interpretation, as well as formatted reports.',
        
      }, // The key-value pairs where the key is the label and value is the content for the textarea
      selectedCheckboxes: ['Encounter', 'Condition', 'Procedure'], // Default selected checkboxes
      loading: false // Loading state
    //   prompts: [],
    //   selectedPrompt: '',
      
    };
  },
  mounted() {
    this.fetchPrompts();
    this.initializePromptText();
    this.updateTextareaWithCheckboxes(); // Initialize promptText with default selected checkboxes
  },
  methods: {
    async fetchPrompts() {
      try {
        let response;
        if (this.selectedPrompt === 'extract') {
          response = await axios.get('http://localhost:8000/api/prompts/extract');
        }
        
        this.prompts = response.data;
        this.updatePromptText();
      } catch (error) {
        console.error('Error fetching prompts:', error);
      }
    },
    updatePromptText() {
      this.promptText = this.prompts + '\n';
      // this.promptText += this.selectedCheckboxes.join('\n');
      // Create a set of existing keys to avoid duplicates
      const existingKeys = new Set(
        this.promptText.split('\n').map(line => line.split(':')[0].trim())
      );

      // Append the default selected checkbox texts in the format "key: content"
      this.selectedCheckboxes.forEach(key => {
        if (this.checkboxTexts[key] && !existingKeys.has(key)) {
          this.promptText += `\n${key}: ${this.checkboxTexts[key]}`;
        }
      });
    },
    initializePromptText() {
      // Create a set of existing keys to avoid duplicates
      const existingKeys = new Set(
        this.promptText.split('\n').map(line => line.split(':')[0].trim())
      );

      // Append the default selected checkbox texts in the format "key: content"
      this.selectedCheckboxes.forEach(key => {
        if (this.checkboxTexts[key] && !existingKeys.has(key)) {
          this.promptText += `\n${key}: ${this.checkboxTexts[key]}`;
        }
      });
    },
    scrollTextareaToBottom() {
      const textarea = this.$refs.promptTextarea;
      if (textarea) {
        textarea.scrollTop = textarea.scrollHeight;
      }
    },
    updateTextareaWithCheckboxes() {
      // Split the current promptText into lines
      const lines = this.promptText.split('\n');

      // Filter out lines that correspond to any deselected checkbox keys
      const updatedLines = lines.filter(line => {
        const key = line.split(':')[0].trim();
        return this.selectedCheckboxes.includes(key) || !this.checkboxTexts[key];
      });

      // Add the selected checkbox texts in the format "key: content" if not already present
      this.selectedCheckboxes.forEach(key => {
        if (this.checkboxTexts[key] && !updatedLines.includes(`${key}: ${this.checkboxTexts[key]}`)) {
          updatedLines.push(`${key}: ${this.checkboxTexts[key]}`);
        }
      });

      // Join the lines back together to form the updated promptText
      this.promptText = updatedLines.join('\n');

      // Scroll to the bottom of the textarea after updating its content
      this.$nextTick(() => {
        this.scrollTextareaToBottom();
      });
    },
    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    },
    
    async sendMessage() {
      if (this.newMessage.trim() === '') return;

      this.loading = true; // Start loading

      this.messages.push({ id: Date.now(), text: this.newMessage, sender: 'user' });
      
      this.promptText_send = ''+this.promptText+'';
      try {
        const response = await axios.post('http://localhost:8000/chat', { message: this.newMessage, prom:this.promptText_send });
        // const botReply = response.data.reply;
        const text_01 = response.data.reply;
        const text_02 = response.data.general;
        this.messages.push({ id: Date.now() + 1, text: text_01, sender: 'bot' });

        // Emit an event with the bot's reply
        this.$emit('bot-reply', text_02);
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        this.loading = false; // Stop loading
      }

      this.newMessage = '';

      // Scroll to the bottom after adding a new message
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    }
  }
};
</script>

<style>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 70vh;
  width: 100%;
  /* max-width: 600px; */
  margin: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
}
.chat-container-prompt {
  display: flex;
  flex-direction: column;
  height: auto;
  min-height: 70vh;
  width: 100%;
  margin: 20px 0;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  /* background-color: #fff; */
}

.alert {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.checkbox-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px; /* Adjusts spacing between checkboxes */
  margin-bottom: 20px;
}

.checkbox-label {
  flex: 1 1 calc(50% - 15px); /* Two columns by default with a 15px gap */
  display: flex;
  align-items: center;
  padding: 10px;
  /* background-color: #f9f9f9;
  border: 1px solid #ddd; */
  border-radius: 4px;
  transition: background-color 0.3s ease;
  cursor: pointer;
  color: white;
  
}

/* .checkbox-label:hover {
  background-color: #e9e9e9;
} */

.checkbox-label input[type="checkbox"] {
  margin-right: 10px;
}

@media (max-width: 768px) {
  .checkbox-label {
    flex: 1 1 100%; /* Full width on small screens */
  }
}

@media (min-width: 1024px) {
  .checkbox-label {
    flex: 1 1 calc(33.33% - 15px); /* Three columns on larger screens */
  }
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 10px;
  padding-right: 10px;
}

.message {
  padding: 8px;
  margin: 4px 0;
  border-radius: 4px;
  max-width: 80%; /* Ensures the messages don’t take up the full width */
}

.message.user {
  align-self: flex-end;
  background-color: #dcf8c6;
  color: black;
}

.message.bot {
  align-self: flex-start;
  background-color: #f1f0f0;
  color: black;
}

.input-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.message-input {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  width: calc(100% - 90px); /* Adjust width based on button size */
  resize: none; /* Prevent resizing */
  min-height: 200px; /* Minimum height for the textarea */
  max-height: 350px; /* Maximum height for the textarea */
  overflow-y: auto; /* Add scroll if content exceeds max-height */
  flex-grow: 1;
  flex-basis: auto;
}
.send-button {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  /* flex-shrink: 0; */
  width: 100%; /* Fixed width for button */
  align-self: flex-end;
}

.send-button:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .message-input {
    width: 100%; /* Full width on smaller screens */
  }

  .send-button {
    width: 100%;
  }

  .input-container {
    flex-direction: column;
    gap: 5px;
  }
}
.promptText {
  width: 100%;
  flex-grow: 1;
  min-height: 200px;
  max-height: 50vh;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow-y: auto;
  font-size: 1rem;
  resize: vertical;
  margin-top: 20px;
}
</style>
