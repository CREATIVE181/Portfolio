from .CONFIG import qiwi_token

from pyqiwip2p import AioQiwiP2P
import asyncio


async def qiwi(callback, price):
    p2p = AioQiwiP2P(auth_key=qiwi_token, default_amount=price)
    new_bill = await p2p.bill(lifetime=10)
    bill_id = new_bill.bill_id
    url = new_bill.pay_url
    await callback.message.edit_text(f'''
To make a payment, follow the link below:
{url}
This link will be valid for 10 minutes!''')

    for _ in range(200):
        check = (await p2p.check(bill_id=bill_id)).status
        if check == "PAID":
            return True
        await asyncio.sleep(3)
    return False


