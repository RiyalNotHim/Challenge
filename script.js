const projectsData = {
    1: {
        name: "Day 01 - Dev Environment Booster",
        readme: "Day 01 - Dev Environment Booster/README.md",
        outputs: ["Day 01 - Dev Environment Booster/Output/Day 1 - Output.png"],
        githubPath: "Day%2001%20-%20Dev%20Environment%20Booster"
    },
    2: {
        name: "Day 02 - Windows Cleanup Assistant",
        readme: "Day 02 - Windows Cleanup Assistant/README.md",
        outputs: ["Day 02 - Windows Cleanup Assistant/docs/Day 2 - Output.png"],
        githubPath: "Day%2002%20-%20Windows%20Cleanup%20Assistant"
    }
};

let currentDay = 1;
let currentSlide = 0;
let totalSlides = 0;

function initializeTabs() {
    const tabsContainer = document.getElementById('tabs');
    
    for (let i = 1; i <= 50; i++) {
        const tab = document.createElement('button');
        tab.className = 'tab';
        tab.textContent = `Day ${i}`;
        tab.dataset.day = i;
        
        if (projectsData[i]) {
            tab.classList.add('completed');
        }
        
        if (i === 1) {
            tab.classList.add('active');
        }
        
        tab.addEventListener('click', () => loadDay(i));
        tabsContainer.appendChild(tab);
    }
}

async function loadDay(day) {
    currentDay = day;
    
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelector(`.tab[data-day="${day}"]`).classList.add('active');
    
    const project = projectsData[day];
    
    if (!project) {
        showEmptyState();
        return;
    }
    
    updateProjectLink(day, project.githubPath);
    
    await loadReadme(project.readme);
    await loadOutputs(project.outputs);
}

function updateProjectLink(day, githubPath) {
    const projectLinkBtn = document.getElementById('projectLink');
    if (githubPath) {
        projectLinkBtn.href = `https://github.com/RiyalNotHim/Challenge/tree/main/${githubPath}`;
        projectLinkBtn.style.display = 'flex';
    } else {
        projectLinkBtn.style.display = 'none';
    }
}

async function loadReadme(readmePath) {
    const readmeContent = document.getElementById('readme-content');
    
    try {
        const response = await fetch(readmePath);
        if (!response.ok) throw new Error('README not found');
        
        const markdown = await response.text();
        readmeContent.innerHTML = marked.parse(markdown);
    } catch (error) {
        readmeContent.innerHTML = '<div class="empty-state">README not available</div>';
    }
}

async function loadOutputs(outputs) {
    const slideshowContainer = document.getElementById('slideshow-images');
    const dotsContainer = document.getElementById('slide-dots');
    
    slideshowContainer.innerHTML = '';
    dotsContainer.innerHTML = '';
    
    if (!outputs || outputs.length === 0) {
        slideshowContainer.innerHTML = '<div class="empty-state">No output available</div>';
        document.getElementById('prevBtn').style.display = 'none';
        document.getElementById('nextBtn').style.display = 'none';
        return;
    }
    
    totalSlides = outputs.length;
    currentSlide = 0;
    
    outputs.forEach((outputPath, index) => {
        const img = document.createElement('img');
        img.src = outputPath;
        img.alt = `Output ${index + 1}`;
        if (index === 0) img.classList.add('active');
        slideshowContainer.appendChild(img);
        
        const dot = document.createElement('span');
        dot.className = 'dot';
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => showSlide(index));
        dotsContainer.appendChild(dot);
    });
    
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (totalSlides > 1) {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
    } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
    }
}

function showSlide(index) {
    const images = document.querySelectorAll('.slideshow-images img');
    const dots = document.querySelectorAll('.dot');
    
    images.forEach(img => img.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    currentSlide = index;
    
    if (images[currentSlide]) {
        images[currentSlide].classList.add('active');
        dots[currentSlide].classList.add('active');
    }
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(currentSlide);
}

function showEmptyState() {
    const readmeContent = document.getElementById('readme-content');
    const slideshowContainer = document.getElementById('slideshow-images');
    
    readmeContent.innerHTML = '<div class="empty-state">Project not yet completed</div>';
    slideshowContainer.innerHTML = '<div class="empty-state">No output available</div>';
    
    document.getElementById('prevBtn').style.display = 'none';
    document.getElementById('nextBtn').style.display = 'none';
    document.getElementById('slide-dots').innerHTML = '';
}

document.getElementById('prevBtn').addEventListener('click', prevSlide);
document.getElementById('nextBtn').addEventListener('click', nextSlide);

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') prevSlide();
    if (e.key === 'ArrowRight') nextSlide();
});

window.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    loadDay(1);
});