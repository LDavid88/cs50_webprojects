document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-view').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><hr>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      //iterate in each item of the dict
      emails.forEach(email => {
        console.log(email);
        const email_section = document.createElement('div');
        email_section.innerHTML = `
        <h5>Sender: ${email["sender"]}</h5>
        <h6>Subject: ${email["subject"]}</h6>
        <p>Timestamp: ${email["timestamp"]}</p><hr>
        `;
        if (email["read"]) {
          email_section.className = 'read'
        } else {
          email_section.className = 'unread'
        }
        email_section.addEventListener('click', function() {
            console.log('This element has been clicked!');
            fetch(`/emails/${email["id"]}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })
        });
        document.querySelector('#emails-view').append(email_section);
      })
        
      });

      // ... do something else with emails ...
}

function send_mail(event) {
  event.preventDefault();
  
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('inbox');
  });
}
