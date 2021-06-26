document.addEventListener('DOMContentLoaded', function() {
	var elList = document.querySelectorAll('.post_textarea');
	elList.forEach(el => el.style.display = "none");
	document.querySelectorAll('#edit_button').forEach(function(button) {
		let textarea_value = button.value
		button.onclick = function() {
			fetch('/sns/post/'+`${textarea_value}`)
			.then(response => response.json())
			.then(post => {
				console.log(post.body);
				elList.forEach(el => el.style.display = "none");
				var abc = document.getElementById(`${textarea_value}`)
				abc.style.display = 'block';
				c = abc.children
				c[1].innerHTML = post.body;
				c[2].addEventListener('click', () => {
					elList.forEach(el => el.style.display = "none");
					e = document.querySelector('#textarea_'+`${textarea_value}`).value
					d = document.querySelector('#post_body_'+`${textarea_value}`)
					d.innerHTML = e
				});
				
		})};
	});
 });

function like_counter(id)  {
		fetch('/sns/like/'+`${id}`)
			.then(response => response.json())
			.then(post => {
				console.log(post.like);
				let counter = post.like
				document.querySelector('#like_'+`${id}`).innerHTML = counter + 1;
			})
			
	};
	
function dislike_counter(id)  {
	fetch('/sns/like/'+`${id}`)
		.then(response => response.json())
		.then(post => {
			console.log(post.like);
			let counter = post.like
			document.querySelector('#like_'+`${id}`).innerHTML = counter - 1;
		})
		
};