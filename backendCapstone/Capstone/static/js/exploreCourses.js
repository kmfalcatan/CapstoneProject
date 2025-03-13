function toggleMenu(menuIcon) {
    menuIcon.classList.toggle("change")
}

const header = document.querySelector('.menubarContainer');
const navbar = document.querySelector('.subMenubarContainer');

header.addEventListener('click', function(){
    if(navbar.classList === 'fadeIn'){
        navbar.classList.remove('fadeIn');
    } else{
        navbar.classList.toggle('fadeIn');
    }
});

function course(){
    const courseButton = document.querySelector(' .courseInfoContainer');

    if(courseButton.style.display === 'none'){
        courseButton.style.display = 'block';
    } else{
        courseButton .style.display = 'none'
    }
}

function course1(){
    const courseButton = document.querySelector(' .courseContainer');

    if(courseButton.style.display === 'none'){
        courseButton.style.display = 'block';
    } else{
        courseButton .style.display = 'none'
    }
}

function feedback(){
    const feedbackButton = document.querySelector(' .courseInfoContainer');

    if(feedbackButton.style.display === 'none'){
        feedbackButton.style.display = 'block';
    } else{
        feedbackButton .style.display = 'none'
    }
}

function addlist(){
    const addlistButton = document.querySelector(' .addListContainer');

    if(addlistButton.style.display === 'none'){
        addlistButton.style.display = 'block';
        clearForm(); 
    } else{
        addlistButton .style.display = 'none'
    }
}

function addlist1(){
    const addlistButton = document.querySelector(' .addListContainer1');

    if(addlistButton.style.display === 'none'){
        addlistButton.style.display = 'block';
    } else{
        addlistButton .style.display = 'none'
    }
}

function open5(){
    const openButton = document.querySelector(' .closeOpen5');

    if(openButton.style.display === 'none'){
        openButton.style.display = 'block';
    } else{
        openButton .style.display = 'none'
    }
}