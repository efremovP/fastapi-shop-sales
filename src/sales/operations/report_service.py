from typing import List
from datetime import date

config = {
	'empty_category_name': 'Без категории',
	'amount_accuracy': 2,
}

class Report():


	def __init__(self):
		self.header_column_list = []
		self.report_data = {}

	def get_result(self) -> tuple:
		result = {"time_points": self.header_column_list} | self.report_data
		    # "buy": self.report_data[TypeOperationEnum.buy],
		    # "sale": self.report_data[TypeOperationEnum.sale]}
		return result

	def add_row(self, row: dict) -> None:
		if row['category'] == '':
			row['category'] = config['empty_category_name']
			# row_date = date.fromisoformat(str(row['date'])).replace(day=1)

		self._add_new_element(row['type'], row['shop'], row['category'], row['name'], row['date'])

		product_revenue = self._get_product_revenue(row['amount'], row['price'])

		self._add_revenue_to_element(row['type'], row['shop'], row['category'], row['name'], row['date'], product_revenue)

	def _add_new_element(self, type: str, shop: str, category: str, name: str,
						 column_date: str) -> None:

		if not type in self.report_data:
			self.report_data[type] = {'total': 0, 'revenue':{}, 'children': {}}

		if not shop in self.report_data[type]['children']:
			self.report_data[type]['children'][shop] =  {'total': 0, 'revenue':{}, 'children': {}}

		if not category in self.report_data[type]['children'][shop]['children']:
			self.report_data[type]['children'][shop]['children'][category] = {'total': 0, 'revenue':{}, 'children': {}}

		if not name in self.report_data[type]['children'][shop]['children'][category]['children']:
			self.report_data[type]['children'][shop]['children'][category]['children'][name] = {'total': 0, 'revenue':{}}

		if not column_date in self.report_data[type]['revenue']:
			self.report_data[type]['revenue'][column_date] = 0

		if not column_date in self.report_data[type]['children'][shop]['revenue']:
			self.report_data[type]['children'][shop]['revenue'][column_date] = 0

		if not column_date in self.report_data[type]['children'][shop]['children'][category]['revenue']:
			self.report_data[type]['children'][shop]['children'][category]['revenue'][column_date] = 0

		if not column_date in self.report_data[type]['children'][shop]['children'][category]['children'][name]['revenue']:
			self.report_data[type]['children'][shop]['children'][category]['children'][name]['revenue'][column_date] = 0

	def _add_revenue_to_element(self, type: str, shop: str, category: str, name: str,
								column_date: str, product_revenue: float) -> None:

		self.report_data[type]['total'] += product_revenue
		self.report_data[type]['revenue'][column_date] += product_revenue

		self._add_date_to_header_column_list(column_date)

		self.report_data[type]['children'][shop]['total'] += product_revenue
		self.report_data[type]['children'][shop]['revenue'][column_date] += product_revenue

		self.report_data[type]['children'][shop]['children'][category]['total'] += product_revenue
		self.report_data[type]['children'][shop]['children'][category]['revenue'][column_date] += product_revenue

		self.report_data[type]['children'][shop]['children'][category]['children'][name]['total'] += product_revenue
		self.report_data[type]['children'][shop]['children'][category]['children'][name]['revenue'][column_date] += product_revenue

	def _add_date_to_header_column_list(self, column_date: str) -> None:
		if not column_date in self.header_column_list:
			self.header_column_list.append(column_date)

	def _get_product_revenue(self, amount: str, price: str) -> float:
		return int(amount) * float(price)


def main():
	header_column_list, report_data = Report().get_from_file()