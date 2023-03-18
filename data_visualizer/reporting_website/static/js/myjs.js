// change tag strong
// const fileUpload = document.querySelector("#file-upload")
// fileUpload.addEventListener("change",(event)=>{
//     const { files } = event.target;
//     console.log("files", files)
//     document.getElementById("file-name").innerHTML = files[0].name;
// })

// active class
window.addEventListener('load', function() {

    $(".main-menu>li>a[href='" + location.pathname + "']").parent().addClass("active").each(function() {

        $(".main-menu>li>a[href='" + $(this).attr("href") + "']").parent().addClass("active")

    });
    console.log("abc")

})