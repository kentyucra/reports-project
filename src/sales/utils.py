import uuid
import base64
from customers.models import Customer
from profiles.models import Profile
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code


def get_salesman_name_from(id):
    salesman = Profile.objects.get(id=id)
    return salesman.user.username


def get_customer_name_from(id):
    customer = Customer.objects.get(id=id)
    return customer.name


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_key(results_by):
    if results_by == '#1':
        key = 'transaction_id'
    elif results_by == '#2':
        key = 'created'
    return key


def get_chart(chart_type, data, results_by, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 4))
    key = get_key(results_by)
    print('key:', key)
    data = data.groupby(key, as_index=False)['total_price'].agg('sum')

    if chart_type == '#1':
        print('bar chart')
        # plt.bar(data['transaction_id'], data['price'])
        sns.barplot(x=key, y='total_price', data=data)
    elif chart_type == '#2':
        print('pie chart')
        plt.pie(data=data, x='total_price', labels=data[key].values)
    elif chart_type == '#3':
        print('line chart')
        plt.plot(
            data[key],
            data['total_price'],
            color='green',
            marker='o',
            linestyle='dashed'
        )
    else:
        print('ups... wrong chart type')
    plt.tight_layout()
    chart = get_graph()
    return chart
