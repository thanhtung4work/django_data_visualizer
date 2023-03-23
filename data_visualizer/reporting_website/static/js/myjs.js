window.addEventListener('load', function() {

    // active class
    $(".main-menu>li>a[href='" + location.pathname + "']").parent().addClass("active").each(function() {

        $(".main-menu>li>a[href='" + $(this).attr("href") + "']").parent().addClass("active")

    });
    
    // change tag strong
    if(document.querySelector("#file-upload")){
        document.querySelector("#file-upload").addEventListener('change',(event)=>{
            const { files } = event.target;
            console.log("files", files);
            (files.length)?
            document.getElementById("file-name").innerHTML = files[0].name:
            document.getElementById("file-name").innerHTML = "Chưa có tệp nào được chọn"
        })
    }
    // handle menu
    document.getElementById("handle-menu").addEventListener('click',()=>{
        
        const className = document.getElementById('menu');
        (className.className.includes("dynamic-menu"))?
        className.classList.remove('dynamic-menu'):
        className.classList.add('dynamic-menu')

        const arrow = document.getElementById('arrow');
        (arrow.className.includes("fa-arrow-right"))?
        arrow.classList.replace('fa-arrow-right','fa-arrow-left'):
        arrow.classList.replace('fa-arrow-left','fa-arrow-right')

    })

    // file not selected
    if(document.getElementById('btn-submit')){
    document.getElementById('btn-submit').addEventListener('click',()=>{
        if(document.getElementById('file-name').innerHTML === "Chưa có tệp nào được chọn"){
            document.getElementById('title-error').innerHTML = "CHƯA CHỌN FILE KIA KÌA"
            document.getElementById('shadow').style.display = "block";
            document.getElementById('file-error').style.display = "block"
            // setInterval(countdown, 1000);
            timeclose()
            setTimeout(closeInform, 3000)
        }
    })}

})
// check file
function closeInform(){
    document.getElementById('title-error').innerHTML = ""
    document.getElementById('shadow').style.display = "none";
    document.getElementById('file-error').style.display = "none"
}
function timeclose(){
    document.getElementById('time').innerHTML = 3
    let time = 2;
    var x = setInterval(function(){
        document.getElementById('time').innerHTML = time
        time--;
        if(time < 0){
            clearInterval(x)
        }
    },1000)
}
function checkFile(){
    const check = " .txt .data .csv .xlsx";
    const fileUpload = document.getElementById('file-upload');
    console.log("abc")
    if(!(fileUpload.files).length){
        document.getElementById('title-error').innerHTML = "CHƯA CHỌN FILE KIA KÌA"
        document.getElementById('shadow').style.display = "block";
        document.getElementById('file-error').style.display = "block"
        // setInterval(countdown, 1000);
        timeclose()
        setTimeout(closeInform, 3000)
        return false
    }else{
        const arr = (fileUpload.files[0].name).split(".");
        console.log(check.includes(arr[arr.length - 1]))
        if(check.includes(arr[arr.length - 1])){
            console.log("true")
            return true
        }else{
            document.getElementById('title-error').innerHTML = "CHỌN FILE ĐÚNG ĐỊNH DẠNG DÙM CÁI"
            document.getElementById('shadow').style.display = "block";
            document.getElementById('file-error').style.display = "block"
            timeclose()
            setTimeout(closeInform, 3000)
            return false
        }
    }
}
