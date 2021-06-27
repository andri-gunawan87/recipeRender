document.addEventListener('DOMContentLoaded', function() {
	

showSlides(slideIndex);
document.querySelector('#btn').addEventListener('click', addform);


// Next/previous controls

});

var slideIndex = 1;
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  console.log(slides)
  slides[slideIndex-1].style.display = "block";
  
}


function toggleEllipsis() {
	var element = document.querySelector("#ellipsis-ex");
	element.classList.toggle("text-desc");
}

function like_counter(id)  {
		fetch('like/'+`${id}`)
			.then(response => response.json())
			.then(post => {
				console.log(post.like);
				let counter = post.like
				document.querySelector('#like_'+`${id}`).innerHTML = counter + 1;				
				document.querySelector(".like").className = 'btn btn-primary active like';
				document.querySelector(".like").disabled = true;
				document.querySelector(".dislike").disabled = false;
				document.querySelector(".dislike").className = 'btn btn-outline-danger dislike';
			})
			
	};
	
function dislike_counter(id)  {
	fetch('like/'+`${id}`)
		.then(response => response.json())
		.then(post => {
			console.log(post.like);
			let counter = post.like
			document.querySelector('#like_'+`${id}`).innerHTML = counter - 1;
			document.querySelector(".dislike").className = 'btn btn-danger active dislike';
			document.querySelector(".dislike").disabled = true;
			document.querySelector(".like").disabled = false;
			document.querySelector(".like").className = 'btn btn-outline-primary like';
			})
		};


document.querySelector('#ingbtn').addEventListener('click', addform);
var form_id = 3;
function addform()  {
	form_id++;
    var input = document.createElement("input");
	input.className = 'form_bahan_list'
	input.id = 'ing-' + form_id;
    input.type = 'text';
    input.name = 'ing';
    input.placeholder = 'bahan ' + form_id;
	document.querySelector('#ingadd').appendChild(input);
  };

document.querySelector('#stepbtn').addEventListener('click', addstep);
var step = 3;
function addstep()  {
	step++;
    var input = document.createElement("textarea");
	input.className = 'form_bahan_list'
	input.id = 'step-' + step;
    input.type = 'text';
    input.name = 'step';
    input.placeholder = 'Langkah ' + step;
	document.querySelector('#stepadd').appendChild(input);
  };
