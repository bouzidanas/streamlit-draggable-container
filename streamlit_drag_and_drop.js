root = window.parent.document;
console.log(root);

let dropZones = [];
let draggedElement = null;
let dragIndex = 0;


function dragStart(event) {
    // console.log('drag start');
    // console.log(event);
    draggedElement = event.target;
}

draggableContainers = root.querySelectorAll('.draggable-parent');
draggableContainers.forEach(container => {
    let parent = container.parentNode;
    while (parent && parent.tagName !== 'BODY') {
        parent = parent.parentNode;
        if (parent.dataset.testid === 'stVerticalBlockBorderWrapper') {
            console.log(parent);
            if (container.classList.contains('no-drag-handle')) {
                parent.draggable = true;
            }
            else {
                parent.querySelectorAll('.drag-handle')?.forEach(handle => {
                    handle.addEventListener('mouseover', function(event) {
                        parent.draggable = true;
                    });
                });
                parent.querySelectorAll('.drag-handle')?.forEach(handle => {
                    handle.addEventListener('mouseout', function(event) {
                        parent.draggable = false;
                    });
                });
            }
            if (container.classList.contains('no-destination')) {
                // if dropZones doesnt contain parent.parentNode, add it
                const dropZone = parent.parentNode;
                if (!dropZones.includes(dropZone)) {
                    dropZones.push(dropZone);
                     // also remove dot if mouse leaves drop container
                     dropZone?.addEventListener('dragleave', function(event) {
                        event.preventDefault();

                        //make cursor/point the copy cursor
                        event.dataTransfer.dropEffect = 'copy';

                        // console.log(event);
                        // console.log(dropZone);
                        let remove = true;
                        let container = event.fromElement;
                        while (container && container.tagName !== 'BODY') {
                            container = container.parentNode;
                            if (container === dropZone) {
                                remove = false;
                            }
                        }
                        if (remove && event.fromElement !== dropZone && !event.fromElement.classList.contains('floating-dot')) {
                            const dots = root.querySelectorAll('.floating-dot');
                            // console.log('remove dots dragleave');
                            dots.forEach(dot => {
                                dot.remove();
                            });
                        }
                    });
                    dropZone?.addEventListener('dragover', function(event) {
                        event.preventDefault();
                        // console.log(event.target);
                        
                        //make cursor/point the copy cursor
                        event.dataTransfer.dropEffect = 'copy';

                        const rect = dropZone.getBoundingClientRect();
                        const y = event.clientY - rect.top;
                        const children = Array.from(dropZone.children);
                        let i = 0;
                        for (const child of children) {
                            // console.log(child.offsetTop + child.offsetHeight / 2, y);
                            if (child.offsetTop + child.offsetHeight / 2 < y) {
                                i++;
                            }
                        }

                        if (i === dragIndex) {
                            return;
                        }
                        else {
                            // remove any floating dots
                            // console.log('remove dots' , i, dragIndex);
                            const dots = root.querySelectorAll('.floating-dot');
                            dots.forEach(dot => {
                                dot.remove();
                            });
                        }
                        dragIndex = i;

                        // console.log(i);
                        if (children[i] !== draggedElement && children[i] !== draggedElement.nextSibling) {
                            const dot = document.createElement('div');
                            dot.style.position = 'absolute';
                            // dot.style.width = '4px';
                            // dot.style.height = '4px';
                            // dot.style.backgroundColor = '#444444';
                            // dot.style.borderRadius = '50%';
                            dot.style.width = '8%';
                            dot.style.height = '4px';
                            dot.style.backgroundColor = '#444444';
                            dot.style.borderRadius = '2px';
                            dot.style.left = '46%';
                            if (i === children.length) {
                                dot.style.top = rect.top + children[i-1].offsetTop + children[i-1].offsetHeight + 10 + 'px';
                            } else {
                                dot.style.top = rect.top + children[i].offsetTop - 10 + 'px';
                            }
                            dot.classList.add('floating-dot');
                            dropZone.parentNode.insertBefore(dot, dropZone);
                        }
                        
                    });
                    dropZone?.addEventListener('drop', function(event) { 
                        event.preventDefault();
                       
                        // remove any floating dots
                        const dots = root.querySelectorAll('.floating-dot');
                        dots.forEach(dot => {
                            dot.remove();
                        });
                        
                        // console.log('drop');
                        // console.log(event);
                        // insert parent at location of drop in dropZone
                        const rect = dropZone.getBoundingClientRect();
                        const y = event.clientY - rect.top;
                        const children = Array.from(dropZone.children);
                        let i = 0;
                        for (const child of children) {
                            // console.log(child.offsetTop + child.offsetHeight / 2, y);
                            if (child.offsetTop + child.offsetHeight / 2 < y) {
                                i++;
                            }
                        }
                        // console.log(i);
                        dropZone.insertBefore(draggedElement, children[i]);
                    });
                }
            }
            parent.addEventListener('dragstart', dragStart);
            break;
        }
    }
});

// hide iframe that contains div with class 'elim' to remove script container from
// potential drop destination and prevent it from interfering with drag and drop
const iframe = root.querySelectorAll('iframe');
iframe.forEach(frame => {
    const div = frame.contentDocument.querySelector('.elim');
    if (frame.parentNode.dataset.testid === 'element-container') {
        frame.parentNode.style.display = 'none';
    }
});

// hide element-container containing div with class 'elim' to hide markdown 
// elements that are added for drag and drop purposes
const elements = root.querySelectorAll('[data-testid="element-container"]');
elements.forEach(element => {
    const div = element.querySelector('.elim');
    if (div) {
        element.style.display = 'none';
    }
});