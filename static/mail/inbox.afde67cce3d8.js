document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', inbox);
  document.querySelector('#sent').addEventListener('click', sent);
  document.querySelector('#archived').addEventListener('click', archive);
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_mail;

  // By default, load the inbox
  inbox();
});

function alert_m(massage) {
	document.querySelector('#alert_m').innerHTML = '';
	document.querySelector('#alert_m').style.display = 'block';
	document.querySelector('#alert_m').innerHTML = massage;
}
	

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#alert_m').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#sent-view').style.display = 'none';
  document.querySelector('#inbox-view').style.display = 'none';
  document.querySelector('#archive-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
   
};

function send_mail() {
	const rec = document.querySelector('#compose-recipients').value;
	const sub = document.querySelector('#compose-subject').value;
	const body = document.querySelector('#compose-body').value;
	fetch('emails', {
		method: 'POST',
		body: JSON.stringify({
			recipients: rec,
			subject: sub,
			body: body
		})
	})
	.then(response => response.json())
	.then(result => {
		// Print result
		sent();
		console.log(result);
		if (result.error === undefined){
			alert_m(result.message);
		} else {
			alert_m(result.error);
		}
		
		
		
	});
	return false;
};

function inbox() {
	document.querySelector('#alert_m').style.display = 'none';
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#sent-view').style.display = 'none';
	document.querySelector('#inbox-view').style.display = 'block';
	document.querySelector('#archive-view').style.display = 'none';
	document.querySelector('#inboxv').innerHTML = '';

	fetch('emails/inbox')
	.then(response => response.json())
	.then(emails => {
    // Print emails
    console.log(emails);	
    // ... do something else with emails ...
	if (emails.length == 0){
			var contain = document.createElement('div');
			contain.className = 'e_inbox';
			contain.innerHTML = 'Your Inbox is Empty';
			document.querySelector('#inboxv').appendChild(contain);
	} else {
		emails.forEach((item) => {
			var contain = document.createElement('div');
			if (item.read == true){
				contain.className = 'read border';
			} else {
				contain.className = 'border';
			}
			contain.innerHTML = `<div class="row">
					<div class="col">
						From: ${item.sender}<br>
						Subject: ${item.subject}
					</div>
					<div class="col col-lg-2">
						${item.timestamp.slice(0, 18)}
					</div>`;
		  
			document.querySelector('#inboxv').appendChild(contain);
			contain.addEventListener('click', () => show_email(item.id));
		  });
			}
})};

function sent() {
	document.querySelector('#alert_m').style.display = 'none';
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#inbox-view').style.display = 'none';
	document.querySelector('#sent-view').style.display = 'block';
	document.querySelector('#archive-view').style.display = 'none';
	document.querySelector('#sentv').innerHTML = '';
	
	fetch('emails/sent')
	.then(response => response.json())
	.then(emails => {
		// Print emails
    console.log(emails);	
    // ... do something else with emails ...
	if (emails.length == 0){
			var contain = document.createElement('div');
			contain.className = 'e_inbox';
			contain.innerHTML = 'Your Sent box is Empty';
			document.querySelector('#sentv').appendChild(contain);
	} else {
		emails.forEach((item) => {
			var contain = document.createElement('div');
			contain.className = 'border';
			contain.innerHTML = `<div class="row">
					<div class='col'>
						From: ${item.sender}<br>
						Subject: ${item.subject}
					</div>
					<div class='col col-lg-2'>
						${item.timestamp.slice(0, 18)}
					</div>
				</div>`;
		  
			document.querySelector('#sentv').appendChild(contain);
			contain.addEventListener('click', () => show_email(item.id, sent));
		  });
	}
})};

function archive() {
	document.querySelector('#alert_m').style.display = 'none';
	document.querySelector('#emails-view').style.display = 'none';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#inbox-view').style.display = 'none';
	document.querySelector('#sent-view').style.display = 'none';
	document.querySelector('#archive-view').style.display = 'block';
	document.querySelector('#arcv').innerHTML = '';
	
	fetch('emails/archive')
	.then(response => response.json())
	.then(emails => {
		// Print emails
    console.log(emails);	
    // ... do something else with emails ...
	if (emails.length == 0){
			var contain = document.createElement('div');
			contain.className = 'e_inbox';
			contain.innerHTML = 'No Email Archived';
			document.querySelector('#arcv').appendChild(contain);
	} else {
	emails.forEach((item) => {
		var contain = document.createElement('div');
		contain.className = 'border';
		contain.innerHTML = `<div class="row">
				<div class="col">
					From: ${item.sender}<br>
					Subject: ${item.subject}
				</div>
				<div class="col col-lg-2">
					${item.timestamp.slice(0, 18)}
				</div>
			</div>`;
	  
		document.querySelector('#arcv').appendChild(contain);
		contain.addEventListener('click', () => show_email(item.id));
      });
	}
})};
	
function show_email(id, status) {
	document.querySelector('#alert_m').style.display = 'none';
	document.querySelector('#emails-view').style.display = 'block';
	document.querySelector('#compose-view').style.display = 'none';
	document.querySelector('#sent-view').style.display = 'none';
	document.querySelector('#inbox-view').style.display = 'none';
	document.querySelector('#archive-view').style.display = 'none';
	document.querySelector('#mailv').innerHTML = '';
	
	fetch('emails/'+`${id}`)
	.then(response => response.json())
	.then(email => {
		// Print email
		console.log(email);
		if (email.read == false) {
				fetch('/emails/'+`${id}`, {
				method: 'PUT',
				body: JSON.stringify({
					read: true
					})
				})
			}
			
		// For Debug function to make email read/unread	
		//	else {
		//		fetch('/emails/'+`${id}`, {
		//		method: 'PUT',
		//		body: JSON.stringify({
		//			read: false
		//			})
		//		})
		//	}
		
		var mail = document.createElement('div');
		if (!(status == sent)) {
			var rec = email.sender
			if (email.archived) {
				var archive_status = '<button class="btn btn-sm btn-outline-primary" id="archive_button">Unarchive</button><br>'
			} else {
				var archive_status = '<button class="btn btn-sm btn-outline-primary" id="archive_button">Archive</button><br>'
			}
				
		} else {
			var archive_status =''
			var rec = email.recipients
		}
		mail.innerHTML = `From: ${email.sender}<br>
		Recipients: ${email.recipients}<br>
		Subject: ${email.subject}<br>
		Date: ${email.timestamp}<br>
		<button class='btn btn-sm btn-outline-primary' id='reply_button'>Reply</button>
		${archive_status}
		<hr />
		${email.body}`;
	  
		document.querySelector('#mailv').appendChild(mail);
			document.querySelector('#reply_button').addEventListener('click', () => {
				if (email.subject.substring(0,4) === 'Re: ') {
					var sub = email.subject
				} else {
					var sub = `Re: ${email.subject}`
				}
			var time = email.timestamp;
			var body = email.body;
			
			compose_email();
			document.querySelector('#compose-recipients').value = rec;
			document.querySelector('#compose-subject').value = sub;
			document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n "${email.body}"\n`;
		});

		document.querySelector('#archive_button').addEventListener('click', () => {
			if (email.archived == false) {
				fetch('emails/'+`${id}`, {
				method: 'PUT',
				body: JSON.stringify({
					archived: true
					})
				})
				massage = 'Email Archived'
			}
			else {
				fetch('emails/'+`${id}`, {
				method: 'PUT',
				body: JSON.stringify({
					archived: false
					})
				})
				massage = 'Email Unarchived'
			}
			// Function "inbox()" sometime work sometime dont
			// This function need delay, so the server have a time to update before serve it to client
			// Pardon my weak CPU
			setTimeout(function() { inbox(); }, 100);
			setTimeout(function() { alert_m(massage); }, 100);
		});
	});
};