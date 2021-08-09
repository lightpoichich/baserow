from django.db.models import Expression, DateTimeField, Value


class Timezone(Expression):
    def __init__(self, expression, timezone):
        super().__init__(output_field=DateTimeField())
        self.source_expression = self._parse_expressions(expression)[0]
        self.timezone = timezone

    def resolve_expression(
        self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
    ):
        c = self.copy()
        c.is_summary = summarize
        c.source_expression = self.source_expression.resolve_expression(
            query, allow_joins, reuse, summarize, for_save
        )
        return c

    def __repr__(self):
        return "{}({}, {})".format(
            self.__class__.__name__,
            self.field_name,
            self.timezone,
        )

    def as_sql(self, compiler, connection):
        params = []
        field_sql, field_params = compiler.compile(self.source_expression)
        timezone_sql, timezone_params = compiler.compile(Value(self.timezone))
        params.extend(field_params)
        params.extend(timezone_params)
        return f"{field_sql} at time zone {timezone_sql}", params


#
# class Timezone(Func):
#     """An SQL function call."""
#
#     function = None
#     template = "%(expressions)s at time zone %(timezone)s"
#     arg_joiner = ", "
#
#     def __init__(self, *expressions, timezone, output_field=None):
#         super().__init__(output_field=output_field)
#         self.timezone = timezone
#         self.source_expressions = self._parse_expressions(*expressions)
#
#     def __repr__(self):
#         args = self.arg_joiner.join(str(arg) for arg in self.source_expressions)
#         extra = {**self.extra, **self._get_repr_options()}
#         if extra:
#             extra = ", ".join(
#                 str(key) + "=" + str(val) for key, val in sorted(extra.items())
#             )
#             return "{}({}, {})".format(self.__class__.__name__, args, extra)
#         return "{}({})".format(self.__class__.__name__, args)
#
#     def _get_repr_options(self):
#         """Return a dict of extra __init__() options to include in the repr."""
#         return {}
#
#     def get_source_expressions(self):
#         print(self.source_expressions)
#         return self.source_expressions
#
#     def set_source_expressions(self, exprs):
#         self.source_expressions = exprs
#
#     def resolve_expression(
#         self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
#     ):
#         c = self.copy()
#         c.is_summary = summarize
#         for pos, arg in enumerate(c.source_expressions):
#             c.source_expressions[pos] = arg.resolve_expression(
#                 query, allow_joins, reuse, summarize, for_save
#             )
#         return c
#
#     def as_sql(
#         self,
#         compiler,
#         connection,
#         function=None,
#         template=None,
#         arg_joiner=None,
#         **extra_context
#     ):
#         connection.ops.check_expression_support(self)
#         sql_parts = []
#         params = []
#         for arg in self.source_expressions:
#             arg_sql, arg_params = compiler.compile(arg)
#             sql_parts.append(arg_sql)
#             params.extend(arg_params)
#         print(params)
#         data = {}
#         template = template or data.get("template", self.template)
#         arg_joiner = arg_joiner or data.get("arg_joiner", self.arg_joiner)
#         data["expressions"] = data["field"] = arg_joiner.join(sql_parts)
#         return template % data, params
#
#     def copy(self):
#         copy = super().copy()
#         copy.source_expressions = self.source_expressions[:]
#         copy.extra = self.extra.copy()
#         return copy
