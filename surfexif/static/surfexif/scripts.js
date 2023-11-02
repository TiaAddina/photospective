/* ... List of relevant JSON-resource url patterns for the Surfexif app ... */

// This is intended to make it easier to update this scripts file in
// case we made changes to the URL patterns for the website
API_url_patterns = {
    tags_categ_json : 'json/tags4cat',
    imgs_w_tags     : 'img/all'
}

/* ... Main Function ... */
document.addEventListener('DOMContentLoaded', function() {

    // If the login, logout, or register buttons are clicked, clear SessionStorage
    document.querySelectorAll('.login-btn, .logout-btn, .register-btn').forEach(user_btn => {
        user_btn.onclick=function () {sessionStorage.clear();};
    })

    // Populate the query bay box with what is stored in session
    refresh_query_bay();

    // Attach functionality to add-tag buttons
    add_tag_functionality ();

    // Attach functionality to category buttons
    document.querySelectorAll('.category-tools .category_btn').forEach(category_btn => {
        category_btn.onclick = function () {reveal_tags_for_category(category_btn);};
    });

    // Attach functionality to buttons for showing/hiding EXIF information tables
    document.querySelectorAll('.infotable_btn').forEach(infotable_btn => {
        infotable_btn.onclick = function () {reveal_infotable(infotable_btn);};
    });

    // Attach functionality to Execute Query button
    query_exec_btn = document.getElementById('queryexecute_btn');
    if (query_exec_btn) {
        query_exec_btn.onclick = function () {execute_query();};
    }

});

/* ... Primary Functions ... */


// Event handler for when execute query button is click
function execute_query () {

    // Construct query string (with GET parameters) from the current tags
    function construct_query () {

        // Specify the ingredients for the query path
        const param_key = `t`

        // Access our API for getting the images that satisfies all tags given
        var query_path = `${host_url()}/${API_url_patterns.imgs_w_tags}?`

        // Retrieve the list of query tags from sessionStorage
        const items = JSON.parse(sessionStorage.getItem('querybay'));

        // If sessionstorage contains a list of tags,
        if (items) {

            // Then append the ids for each tag to the base URL path
            Object.keys(items).forEach(key => {
                const tag_param = `&${param_key}=${items[key][1]}`;
                query_path = query_path + tag_param;
            });

            // Once all tag ids are appended, return the full path
            return query_path;
        
        // If there is no query list stored, then don't refresh the page
        } else {
            return '#void'
        }
    }

    // Load the URL path specified
    window.location.href = `${construct_query()}`;
    
    // Clear sessionStorage since we want to start fresh
    sessionStorage.clear();
}


// Event handler for when show/hide infotable buttons are clicked
function reveal_infotable (infotable_btn){
    
    // Event handler for hiding the EXIF information table
    function hide_infotable (infotable_btn) {
        infotable = document.getElementById(`img-infotable-${infotable_btn.dataset.imageid}`);
        infotable.style.display = 'none';
        infotable_btn.onclick =  function () {reveal_infotable(infotable_btn);};
    }
    
    // Select the correct table for the button that was clicked 
    infotable = document.getElementById(`img-infotable-${infotable_btn.dataset.imageid}`);
    
    // Display the table
    infotable.style.display = 'block';
    
    // Switch button functionality to hide the table the next time 
    // the button is clicked
    infotable_btn.onclick =  function () {hide_infotable(infotable_btn);};
}


// Function for attaching functionality to add-tag buttons
function add_tag_functionality () {

    // Select all of the add-tag buttons currently on the page and attach
    // the relevant functionality
    document.querySelectorAll('.add_tag_btn').forEach(tag_btn => {
        
        // When add-tag button is clicked, the tag is added to the
        // list of queries to be executed from the query bay
        tag_btn.onclick = function () {add_tag_to_query(tag_btn);};
    });

    // Event handler for when add-tag buttons are clicked
    function add_tag_to_query(tag_btn) {

        // Update the query bay with the appropriate tag id and tag descriptor
        update_query_bay(`${tag_btn.dataset.tagcategory}`, `${tag_btn.dataset.tagname}`, `${tag_btn.dataset.tagid}`);

        // Insert the user query data into the query bay container
        refresh_query_bay();        
    }

    // Function for updating the query bay as stored in SessionStorage
    function update_query_bay (tag_category, tag_descriptor, tag_id ) {

        /*
         In this source, I reviewed what Session Storage is, and its
         similarities/differences with the LocalStorage seen in class.
         https://www.w3schools.com/jsref/prop_win_sessionstorage.asp

         In the source below, I learned how to use JSON.parse and JSON.stringify
         to store and retrieve JSON objects in SessionStorage:
         https://stackoverflow.com/questions/52409418/pushing-an-element-to-an-existing-array-stored-in-session-storage

         I decided to use SessionStorage over LocalStorage because I didn't want
         the query tags to exist for too long in the web browser
        
         In the source below, I learned how to use "Object.assign" to more
         elegant append items to pre-existing JSON objects
         https://stackoverflow.com/questions/28527712/how-to-add-key-value-pair-in-the-json-object-already-declared/28527898
        */

         // The code below is an amalgamation of all the techniques learned
         // in the three sources above:

         // Check if SessionStorage entry for our list of queries exists,
        if(sessionStorage.getItem('querybay') === null) {
            
            //  If sessionstorage doesn't exist,
            // then initialize an entry in it
            sessionStorage.setItem('querybay', JSON.stringify({ [tag_category] : [ tag_descriptor, tag_id] }));
        
        // If list exists, then append the current tag
        } else {

            // Get the list as an easy-to-use JSON object
            const items = JSON.parse(sessionStorage.getItem('querybay'));
            
            
            /*  Note that this automatically handles duplicate entries
                Shared keys will simply be overwritten.
                This makes sense: Since we are using AND logic, there is no
                reason to use two instances of the same tag - E.g., 
                There could never be an image that is taken with BOTH a 
                NIKON D7000 and a NIKON D3S.
            */
           // Add the new tags to the list 
            Object.assign(items,{[tag_category] : [ tag_descriptor, tag_id]});
            
            // Update the stored list in SessionStorage
            sessionStorage.setItem('querybay', JSON.stringify(items));
        }
    }

}

// Function for refreshing the contents of the query-list box
function refresh_query_bay(){

    // Get the query bay container
    querybay_container = document.getElementById('querybay');

    // Get the query list from sessionstorage
    const items = JSON.parse(sessionStorage.getItem('querybay'));
    
    // If the list exists,
    if (items) {

        // Clear what is currently in the container
        querybay_container.innerHTML = '';

        // Update the container with the new set of queries
        Object.keys(items).forEach(key => {
            querybay_container.insertAdjacentHTML ('afterbegin',
            `
            <button class="querytag_btn btn btn-primary btn-sm bg-success">
                <a  href="${host_url()}/${API_url_patterns.imgs_w_tags}?t=${key}">
                    <b>${key}</b> : ${items[key][0]}
                </a>
            </button>
            `);
        });
    
    // If the list does not exist,
    } else {

        // Just clear what is currently in the container
        if (querybay_container) {
            querybay_container.innerHTML = '';
        }
    }
}

// Event handler for when category buttons are clicked
function reveal_tags_for_category(category_btn) {

    // Get the necessary pieces of data for creating the
    // event listeners for the category buttons
    const cat_ID=category_btn.dataset.categoryid;
    const img_ID=category_btn.dataset.imageid;
    const tags_box_ID = `tags-box-${cat_ID}-${img_ID}`

    // Event handler for when clicked category links are clicked again
    function hide_tags_for_category(category_btn) {
        
        // Remove the tags box if the user doesn't want to see it anymore
        document.getElementById(`${tags_box_ID}`).remove();

        // Reattach functionality for generating the tags box again
        category_btn.onclick = function () {reveal_tags_for_category(category_btn);};
    }

    // Set onclick to functionality to hide tags
    category_btn.onclick = function () {hide_tags_for_category(category_btn);};

    // Create box for tags
    document.getElementById(`category-tools-${cat_ID}-${img_ID}`).insertAdjacentHTML('afterend',`<div id="${tags_box_ID}"></div>`);

    // For that category, fetch the list of tags
    const API_URL = `${host_url()}/${API_url_patterns.tags_categ_json}/${cat_ID}` 
    fetch(`${API_URL}`)
    .then(response => response.json())
    .then(taglist => {

        // If the category does not exist,
        // quit the function
        if (taglist.error) {
            return;
        } else {

            // Select the correct box for inserting the tags for the category
            const tags_box = document.getElementById(`${tags_box_ID}`);

            // Iterate through the list of tags to generate add-tag buttons
            taglist.forEach(tag => {

                // Technique for appending data using insertAdjacentHTML
                // instead of innerHTML learned from the resource below:
                // https://stackoverflow.com/questions/5677799/how-to-append-data-to-div-using-javascript                
                tags_box.insertAdjacentHTML ('afterbegin', 
                `
                <div>
                    <span class="add_tag_btn" data-tagid="${tag.id}" data-tagname="${tag.descriptor}" data-tagcategory="${category_btn.dataset.categoryname}"> 
                        ➕ 
                    </span>
                    <span>
                        <a  href="${host_url()}/${API_url_patterns.imgs_w_tags}?t=${tag.id}"
                            data-tagid="${tag.id}"
                            data-tagname="${tag.descriptor}"
                        >
                            ${tag.descriptor}
                        </a>
                    </span>
                 <div>
                `);
            });

            // Attach add-tag functionality for newly generated add-tag buttons
            add_tag_functionality ();
        }
    });

}


/* ... Helper Functions ... */

// Function for getting the full path of the host url
// This is used to construct API paths
function host_url () {
    return `${window.location.protocol}//${window.location.host}`
}

