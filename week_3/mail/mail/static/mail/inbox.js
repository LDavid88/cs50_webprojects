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
  document.querySelector('#view-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#view-email').style.display = 'block';
      
      document.querySelector('#view-email').innerHTML = `
      <h5>From: ${email["sender"]}</h5>
      <h6>Recipients: ${email["recipients"]}</h6>
      <h6>Subject: ${email["subject"]}</h6><hr><br>
      <p>${email["body"]}</p><hr>
      <p>${email["timestamp"]}</p>
      `;

      if (!email["read"]) {
        fetch(`/emails/${email["id"]}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        });
      }

      //add button
      const btn = document.createElement('button');
      btn.className = 'btn btn-primary';
      if (email["archived"]) {
        btn.innerHTML = 'Unarchive';
      } else {
        btn.innerHTML = 'Archive';
      };
      btn.addEventListener('click', function() {
        fetch(`/emails/${email["id"]}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email["archived"]
          })
        })
        .then(() => load_mailbox('archive'));
      });
      document.querySelector('#view-email').append(btn);

      //add reply
      const btn_reply = document.createElement('button');
      btn_reply.className = 'btn btn-dark';
      btn_reply.innerHTML = 'Reply';
      btn_reply.addEventListener('click', function() {
        compose_email();
        document.querySelector('#compose-recipients').value = email['sender'];
        if (email['subject'].split(' ', 1) == 'Re' | email['subject'].split(' ', 1) == 're') {
          document.querySelector('#compose-subject').value = `${email['subject']}`;
        } else {
          document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
        }
        document.querySelector('#compose-body').value = `On ${email['timestamp']} ${email['sender']} wrote: ${email['body']}`;
      });
      document.querySelector('#view-email').append(btn_reply);
  });     
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

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
          view_email(email["id"]);
        });
        document.querySelector('#emails-view').append(email_section);
      });
        
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
