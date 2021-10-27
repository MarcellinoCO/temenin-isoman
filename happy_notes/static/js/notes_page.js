console.log('hellow')

const notesBox = document.getElementById('notes-box')
const spinnerBox = document.getElementById('spinner-box')

const noteForm = document.getElementById('note-form')
const sender = document.getElementById('id_sender')
const title = document.getElementById('id_title')
const message = document.getElementById('id_message')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const alertBox = document.getElementById('alert-box')

$.ajax ({
  type: 'GET',
  url: 'data/',
  success: function(response){
      console.log(response)
      const data = response.data
      setTimeout(() => {
        spinnerBox.classList.add('not-visible')
        console.log(data)
        data.forEach(element => {
          notesBox.innerHTML += `
            <div class="col-lg-3 col-md-6 my-4">
                <div class="card" style="width: 18rem">
                    <div class="card-body">
                        <h5 class="card-title text-center">${element.title}</h5>
                        From: ${element.sender}
                        <p class="card-text">
                            <br>
                            ${element.message}
                        </p>
                    </div>
                </div>
            </div>
          `
        });
      }, 100);
  },
  error: function(error){
      console.log(error)
  }
})

noteForm.addEventListener('submit', e=>{
  e.preventDefault()

  $.ajax({
    type:'POST',
    url: '',
    data: {
      'csrfmiddlewaretoken': csrf[0].value,
      'sender': sender.value,
      'title': title.value,
      'message': message.value
    },
    success: function(response) {
      console.log(response)
      notesBox.insertAdjacentHTML('afterBegin', `
        <div class="col-lg-3 col-md-6 my-4">
          <div class="card" style="width: 18rem">
              <div class="card-body">
                  <h5 class="card-title text-center">${response.title}</h5>
                  From: ${response.sender}
                  <p class="card-text">
                      <br>
                      ${response.message}
                  </p>
              </div>
          </div>
        </div>
      `)
      $('#addNotesModul').modal('hide')
      handelAlert('success', 'New note added!')
      noteForm.reset()
    },
    error: function(error){
      console.log(error)
      handelAlert('danger', 'Oopsie! something went wrong')
    }
  })
})