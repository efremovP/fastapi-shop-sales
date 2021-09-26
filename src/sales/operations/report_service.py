from datetime import date

report_config = {
	'empty_category_name': 'Без категории',
	'buy': 'Покупки',
	'sale': 'Продажи',
}

class Report():


	def __init__(self):
		self.header_column_list = []
		self._report_data = {}

	def get_result(self) -> tuple:
		view_report_data = self._make_view_format({})
		result = {"time_points": self.header_column_list} | view_report_data

		return result

	def add_row(self, row: dict):

		category = row['category'] or report_config['empty_category_name']

		row_date = date.fromisoformat(str(row['date'])).replace(day=1)

		self._add_new_element(row['type'], row['shop'], category, row['name'], row_date)

		amount = row['amount'] * row['price']

		self._add_revenue_to_element(row['type'], row['shop'], category, row['name'], row_date, amount)

	def _add_new_element(self, type: str, shop: str, category: str, name: str,  column_date: str):

		if not type in self._report_data:
			self._report_data[type] = {'name': report_config[type.value], 'amounts': {}, 'total_amount': 0, 'children': {}}

		if not shop in self._report_data[type]['children']:
			self._report_data[type]['children'][shop] = {'name': shop, 'amounts': {}, 'total_amount': 0, 'children': {}}

		if not category in self._report_data[type]['children'][shop]['children']:
			self._report_data[type]['children'][shop]['children'][category] = {'name': category, 'amounts': {}, 'total_amount': 0, 'children': {}}

		if not name in self._report_data[type]['children'][shop]['children'][category]['children']:
			self._report_data[type]['children'][shop]['children'][category]['children'][name] = {'name': name, 'amounts': {}, 'total_amount': 0}

		if not column_date in self._report_data[type]['amounts']:
			self._report_data[type]['amounts'][column_date] = 0

		if not column_date in self._report_data[type]['children'][shop]['amounts']:
			self._report_data[type]['children'][shop]['amounts'][column_date] = 0

		if not column_date in self._report_data[type]['children'][shop]['children'][category]['amounts']:
			self._report_data[type]['children'][shop]['children'][category]['amounts'][column_date] = 0

		if not column_date in self._report_data[type]['children'][shop]['children'][category]['children'][name]['amounts']:
			self._report_data[type]['children'][shop]['children'][category]['children'][name]['amounts'][column_date] = 0

	def _add_revenue_to_element(self, type: str, shop: str, category: str, name: str, column_date: str, amount: float):
		self._report_data[type]['total_amount'] += amount
		self._report_data[type]['amounts'][column_date] += amount

		self._add_date_to_header_column_list(column_date)

		self._report_data[type]['children'][shop]['total_amount'] += amount
		self._report_data[type]['children'][shop]['amounts'][column_date] += amount

		self._report_data[type]['children'][shop]['children'][category]['total_amount'] += amount
		self._report_data[type]['children'][shop]['children'][category]['amounts'][column_date] += amount

		self._report_data[type]['children'][shop]['children'][category]['children'][name]['total_amount'] += amount
		self._report_data[type]['children'][shop]['children'][category]['children'][name]['amounts'][column_date] += amount

	def _add_date_to_header_column_list(self, column_date: str):
		if not column_date in self.header_column_list:
			self.header_column_list.append(column_date)

	def _make_view_format(self, view_report_data):
		for type in self._report_data:
			self._report_data[type]['amounts'] = list(self._report_data[type]['amounts'].values())
			self._report_data[type]['children'] = self._iter_result_dict(self._report_data[type]['children'])
			view_report_data = view_report_data | {type: self._report_data[type]}

		return view_report_data

	def _iter_result_dict(self, values):
		result_values = list()
		for value in values:
			local_values = values[value]
			local_values['amounts'] = list(local_values['amounts'].values())
			if 'children' in local_values:
				local_values['children'] = self._iter_result_dict(local_values['children'])

			result_values.append(local_values)

		return result_values