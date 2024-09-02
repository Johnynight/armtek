import asyncio
# from Armtek import Armtek

from asinc_armtek import Armtek


cookies = {
    'VKORG': '8000',
    'rPrice': '0',
    '_ym_uid': '1724249685411255589',
    '_ym_d': '1724249685',
    'ci_sessions': '9ism77b2lll0i7fs2khv3b1bjt5acvt4',
    'REMMEID': 'b44301396954c1a59c67ae92084a3e2c',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
}

# a = Armtek(
#             articles='_SELECT_ps_part_number_pb_name_FROM_product_skus_ps_INNER_JOIN_p.csv',
#             cookies=cookies
#            )
# a.run_2()
#

armtek = Armtek('_SELECT_ps_part_number_pb_name_FROM_product_skus_ps_INNER_JOIN_p.csv', cookies=cookies)
asyncio.run(armtek.run_2())