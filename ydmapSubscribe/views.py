from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .funMain import *


@require_GET
def function_view(request, function_name):
    functions = {
        'GetSalesIds': GetSalesIds,
        'Get3DaysVenue': Get3DaysVenue,
        'GetSalesTimes': GetSalesTimes,
        'SubscribeMap': SubscribeMap,
    }

    function = functions.get(function_name)

    if not function:
        return JsonResponse({'error': 'Function not found'}, status=404)

    # 获取所有 GET 参数
    params = request.GET.dict()

    try:
        # 调用函数并传递参数
        result = function(**params)
        return JsonResponse(result, safe=False)
    except TypeError as e:
        # 参数不匹配
        return JsonResponse({'error': str(e)}, status=400)
