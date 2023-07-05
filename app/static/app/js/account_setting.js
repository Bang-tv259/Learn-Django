var tabPanes = document.getElementsByClassName('tab-pane')
var a_tabPanes = document.getElementsByClassName('a-tab-pane')

for (i = 0; i < a_tabPanes.length; i++)
{        
    
    a_tabPanes[i].addEventListener('click', function (event) {
        var href = this.getAttribute('href')

        var a_tabPanes_new = document.getElementsByClassName('a-tab-pane')
        for (j = 0; j < a_tabPanes_new.length; j++){
            if (a_tabPanes_new[j].classList.contains('active')) a_tabPanes_new[j].classList.remove('active')
        }

        this.classList.add('active')
        show_tabPane(href)

    }) 
}


function show_tabPane(href)
{
    for (j = 0; j < tabPanes.length; j++){
            if( tabPanes[j].classList.contains('active'))  tabPanes[j].classList.remove('active')
            if (tabPanes[j].classList.contains('show')) tabPanes[j].classList.remove('show')
            
            if (('#' + tabPanes[j].getAttribute('id')) === href)
                tabPanes[j].classList.add('active', 'show')
        } 
}