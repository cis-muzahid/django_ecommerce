

function review(n, reviewId) {
    if (reviewId){
        remove(reviewId);
        stars = document.getElementsByClassName("star review_" + reviewId);
        let output = document.getElementById("output_" + reviewId);
        for (let i = 0; i < n; i++) {
            let cls;
            if (n == 1) cls = "one";
            else if (n == 2) cls = "two";
            else if (n == 3) cls = "three";
            else if (n == 4) cls = "four";
            else if (n == 5) cls = "five";
            stars[i].className = "star review_" + reviewId + " " + cls;
        }
        output.value = n;
    }
    else{
        remove();
        stars = document.getElementsByClassName("star");
        let output = document.getElementById("output");
        for (let i = 0; i < n; i++) {
            let cls;
            if (n == 1) cls = "one";
            else if (n == 2) cls = "two";
            else if (n == 3) cls = "three";
            else if (n == 4) cls = "four";
            else if (n == 5) cls = "five";
            stars[i].className = "star " + cls;
        }
        output.value = n;
    }

}

function remove(reviewId) {
    if (reviewId){
        let stars = document.getElementsByClassName("star review_" + reviewId);
        for (let i = 0; i < 5; i++) {
            stars[i].className = "star review_" + reviewId;
        }
    }
    else{
        stars = document.getElementsByClassName("star");
        let i = 0;
        while (i < 5) {
            stars[i].className = "star";
            i++;
        }
    }
}