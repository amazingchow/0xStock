# -*- coding: utf-8 -*-
from mako.template import Template
from mako.lookup import TemplateLookup


def render_create_stock_data_table_up_sql():
    lookup = TemplateLookup(
        directories=["./migrations"],
        output_encoding='utf-8', input_encoding='utf-8',
        default_filters=['decode.utf8'], encoding_errors='replace',
    )
    
    for prefix_code in ["000", "600", "601", "603", "605"]:
        template = lookup.get_template("/create_stock_data_table_up.sql.template")
        values = {
            "stock_code_prefix": prefix_code,
        }
        content = template.render(**values)
        content = str(content, encoding = "utf8")
        with open("./migrations/create_stock_code_prefix_{}_table_up.sql".format(prefix_code), "w") as fw:
            fw.write(content)

        template = lookup.get_template("/create_stock_data_table_down.sql.template")
        values = {
            "stock_code_prefix": prefix_code,
        }
        content = template.render(**values)
        content = str(content, encoding = "utf8")
        with open("./migrations/create_stock_code_prefix_{}_table_down.sql".format(prefix_code), "w") as fw:
            fw.write(content)


if __name__ == "__main__":
    render_create_stock_data_table_up_sql()
