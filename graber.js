global_time_gap = 1000 // ms 抢课间隔

let global_studentCode = JSON.parse(sessionStorage.studentInfo).code;
let global_electiveBatch = "";

function get_electiveBatchCode(studentCode=global_studentCode) { //获取选课轮次
    let data = JSON.parse(sessionStorage.studentInfo);
    let electiveBatch_list = data.electiveBatchList;
    for(let electiveBatch in electiveBatch_list){
        console.log(`${electiveBatch_list[electiveBatch].name} : ${electiveBatch_list[electiveBatch].code}`);
    }
    global_studentCode = data.code;
    global_electiveBatch = electiveBatch_list[0].code; //默认为第一个轮次
}

function get_favorite_and_grab(grab_func, studentCode=global_studentCode, electiveBatchCode=global_electiveBatch) { //获取收藏列表
    $.ajax(
        {
            url : "https://xk.nju.edu.cn/xsxkapp/sys/xsxkapp/elective/queryfavorite.do",
            type :"post",
            headers : {"token":sessionStorage.token},
            data: {
                "querySetting": `{"data":` +
                    `{"studentCode":"${studentCode}",` +
                    `"electiveBatchCode":"${electiveBatchCode}",` +
                    `"teachingClassType":"SC",` +
                    `"queryContent":""},` +
                    `"pageSize":"99",` +
                    `"pageNumber":"0",` +
                    `"order":"isChoose -"}`
            },
            success:function(data) {
                let course_list = data.dataList;
                grab_func(course_list);
            }
        }
    );
}

function print_favorite() { // 打印收藏列表，获取课程编码，轮次，courseKind, teachingClassType，等信息
    get_favorite_and_grab((course_list) => {
        console.log(course_list)
    });
}

function status_clear(studentCode) { //清空状态，防止"请按顺序选课"
    $.ajax(
        {
            url : "https://xk.nju.edu.cn/xsxkapp/sys/xsxkapp/elective/studentstatus.do",
            type :"post",
            headers : {"token":sessionStorage.token},
            data: {
                "studentCode": studentCode,
                "type": "1"
            }
        }
    );
}

function grab(teachingClassId, courseKind, teachingClassType, studentCode=global_studentCode, electiveBatchCode=global_electiveBatch) { //抢课
    /*
        跨专业:  "courseKind":"12","teachingClassType":"KZY"
        体育:    "courseKind":"2","teachingClassType":"TY"
        公选:    "courseKind":"6","teachingClassType":"GG01"
        通识:    "courseKind":"7","teachingClassType":"GG02"
        阅读:    "courseKind":"8","teachingClassType":"YD"
    */
    status_clear(studentCode);
    $.ajax(
        {
            url : "https://xk.nju.edu.cn/xsxkapp/sys/xsxkapp/elective/volunteer.do",
            type :"post",
            headers : {"token":sessionStorage.token},
            data: {"addParam": `{"data":{` +
                `"operationType" : "1",` +
                `"studentCode" : "${studentCode}",` +
                `"electiveBatchCode" : "${electiveBatchCode}",` +
                `"teachingClassId" : "${teachingClassId}",` +
                `"courseKind": "${courseKind}",` +
                `"teachingClassType":"${teachingClassType}"}}`
            },
            success:function(data){
                console.log(data);
                status_clear(studentCode);
            },
        }
    );
    
}

function grab_from_list(course_list) { //从列表中抢课
    for(let course_id in course_list) {
        let course = course_list[course_id];
        grab(
            course.teachingClassID,
            course.courseKind,
            course.teachingClassType,
            global_studentCode,
            course.electiveBatchCode
        );
    } 
}

function grab_from_list_loop(course_list, time_gap) { //从列表循环抢课
    function grab_func() {
        grab_from_list(course_list);
        setTimeout(grab_func, time_gap);
    }
    grab_func();
}

function grab_favorite(time_gap=global_time_gap) { //在收藏列表中循环抢课，参数为抢课间隔时间，只需在控制台调用该函数即可抢课
    get_electiveBatchCode();
    get_favorite_and_grab((course_list) => {
        grab_from_list_loop(course_list, time_gap)
    });
}
