
html_template = """

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>接口自动化测试报告</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 引入 Bootstrap -->
    <!--    <link href="https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">-->
    <link href="/sdp_automation/reports/myreports/css/bootstrap.min.css" rel="stylesheet">
    <link href="/sdp_automation/reports/myreports/layui/css/layui.css" rel="stylesheet">
    <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
    <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
    <!--[if lt IE 9]>
<!--    <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>-->
<!--    <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>-->
    <![endif]-->
    <style type="text/css">
        .hidden-detail, .hidden-tr {{
            display: none;
        }}
    </style>
    <script type="text/javascript" src="js/jquery-1.8.0.min.js"></script>
    <script type="text/javascript" src="js/echarts.common.min.js"></script>
    <script src="/sdp_automation/reports/myreports/layui/layui.js"></script>
</head>
<body>

<div style="padding: 15px">
    <h1>接口测试的结果</h1>
    <table class="table table-hover table-condensed">
        <tbody>
        <tr>
            <td><strong>测试人员:</strong> {tester}</td>
        </tr>
        <tr>
            <td><strong>开始时间:</strong> {start_time}</td>
        </tr>
        <td><strong>结束时间:</strong> {end_time}</td>
        </tr>
        <tr>
            <td><strong>耗时:</strong> {times}s</td>
        </tr>
        <tr>
            <td><strong>结果:</strong>
                <span>
                all:<strong>{all_num}</strong>
                Pass: <strong>{pass_num}</strong>
			Fail: <strong>{fail_num}</strong>
			exception: <strong>{abnormal_num}</strong>
            </span>
            </td>
        </tr>
        </tbody>
    </table>
    <div id="myChartArea" style="width: 600px; height:400px;"></div>
    <div>
        <div id="button-wrap">
            <div class="layui-btn type-button" data-type="all">所有用例</div>
            <div class="layui-btn layui-btn-normal type-button" data-type="success">成功用例</div>
        </div>
        <div id="layer-table"></div>
    </div>
</div>
<script src="https://code.jquery.com/jquery.js"></script>
<script>
    layui.use('table', function () {{
        var table = layui.table;

        console.log(table)

        const renderTable = (data) => {{
            table.render({{
                elem: '#layer-table'
                , height: 312
                , data
                , page: true //开启分页
                , cols: [[ //表头
                    {{field: 'id', title: '用例ID', width: 90, sort: true, fixed: 'left'}}
                    , {{field: 'name', title: '用例名称'}}
                    , {{field: 'requests_data', title: '请求数据'}}
                    , {{field: 'path', title: '路径'}}
                    , {{field: 'method', title: '请求方法',width:90}}
                    , {{field: 'resp', title: '请求响应'}}
                    , {{field: 'assert_result', title: '断言结果'}}
                    , {{field: 'api_times', title: '接口耗时'}}
                    , {{field: 'case_result', title: '测试结果'}}
                ]]
            }});
        }};

        const renderButton = (buttonList) => {{
            let btnHtml = buttonList.map(item => {{
                return `<button class="layui-btn ${{item.class}} type-button" data-type="${{item.type}}" onclick="">${{item.name}}</button>`
            }});
            console.log(btnHtml)
            $("#button-wrap").html(btnHtml);
        }}

        const genData = (type = '所有用例', count = 20) => {{
            let data = [];
            for (i = 0; i < count; i++) {{
                data.push({{
                    name: type + i,
                    id: i,
                    path: type + '地址' + i
                }})
            }}
            return data;
        }}

        let all_case_data = {all_case}
        let success_case_data = {success_case}
        let fail_case = {fail_case}
        let abnormal_case = {abnormal_case}

        const buttonData = [
            {{
                class: '',
                name: '所有用例',
                type: 'all',
                data: all_case_data
            }},
            {{
                class: 'layui-btn-normal',
                name: '成功用例',
                type: 'success',
                data: success_case_data
            }},
            {{
                class: 'layui-btn-warm',
                name: '失败用例',
                type: 'fail',
                data: fail_case,
            }},
            {{
                class: 'layui-btn-danger',
                name: '异常用例',
                type: 'abnormal',
                data: abnormal_case

            }}
        ];


        $("#button-wrap").delegate('.type-button', 'click', function () {{
            let type = $(this).data('type');
            let clickButtonData = buttonData.find(item => item.type === type);
            let tableData = [];
            if (tableData) {{
                tableData = clickButtonData.data || [];
            }} else {{
                tableData = [];
            }}
            renderTable(tableData);
        }});

        renderButton(buttonData);
        renderTable(buttonData[0].data || []);
    }});
</script>
<script type="text/javascript">
    $("#check-danger").click(function (e) {{
        $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
    }});
    $("#check-warning").click(function (e) {{
        $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
    }});
    $("#check-success").click(function (e) {{
        $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".error").addClass("hidden-tr");
    }});
    $("#check-except").click(function (e) {{
        $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".success").addClass("hidden-tr");
    }});
    $("#check-all").click(function (e) {{
        $(".case-tr").removeClass("hidden-tr");
    }});
</script>
<script type="text/javascript">


$(function () {{
    // 为echarts对象加载数据
    myChart.setOption(option);
}});

/**
 * echarts.init(dom容器):基于dom容器,实例化echarts对象
 * dom容器必须是html的节点，如果是使用jQuery获取的则必须指定集合中的一个元素节点，比如(“#main”)则表示jQuery对象。$(“#main”)[0]则表示一个id为main的节点
 */
// var myChart = echarts.init(document.getElementById("myChartArea"));
var myChart = echarts.init($("#myChartArea")[0]);

var option = {{
    title: {{
        text: '本次测试情况',
        subtext: 'By_tester({tester})',
        x: 'center'
    }},
    tooltip: {{
        trigger: 'item',
        formatter: "{{a}} <br/>{{b}} : {{c}} ({{d}}%)"
    }},
    legend: {{
        orient: 'vertical',
        left: 'left',
        data: ['成功用例数', '失败用例数', '异常用例数']
    }},
    series: [
        {{
            name: '测试情况',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
                {{value: {success_num}, name: '成功用例数'}},
                {{value: {pass_num}, name: '失败用例数'}},
                {{value: {abnormal_num}, name: '异常用例数'}},
            ],
            itemStyle: {{
                emphasis: {{
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }}
            }}
        }}
    ]
}};






</script>
</body>
</html>





"""


def to_generate_test_report(all_case, success_case, fail_case, abnormal_case,
                            tester, start_time, end_time, times,
                            pass_num, fail_num,
                            abnormal_num, filepath, all_num):
    """

    :param all_case: 所有用例数据 格式 [{id='1',name:'登录后台'....},{id:'1',name:'2'}]
    :param success_case: 成功用例数据 格式 [{id='1',name:'登录后台'....},{id:'1',name:'2'}]
    :param fail_case: 失败用例数据，格式同上
    :param abnormal_case: 异常用例数据，格式同上
    :param tester: 测试人员
    :param start_time: 开始测试时间
    :param end_time: 结束测试时间
    :param times: 累计耗费时间
    :param all_num: 用例总数
    :param pass_num: 测试通过数
    :param fail_num: 测试失败数
    :param abnormal_num: 异常数
    :param filepath: 文件报告路径
    """
    report_html = html_template.format(all_case=all_case, fail_case=fail_case, abnormal_case=abnormal_case,
                                       tester=tester, start_time=start_time, end_time=end_time, times=times,
                                       pass_num=pass_num, fail_num=fail_num, abnormal_num=abnormal_num,
                                       success_case=success_case, all_num=all_num, success_num=pass_num)
    with open(filepath, 'wb') as f:
        f.write(report_html.encode('utf-8'))
