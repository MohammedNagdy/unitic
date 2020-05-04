# the financial accounts of the user entries

FIN_CHOICES = [
        ("inventory", "مخزون"),
        ("revenue", "المبيعات"),
        ("employee_expense","مرتبات الموظفين"),
        ("cost_of_sales","تكلفة المبيعات"),
        ("research_and_development", "تطوير وبحث"),
        ("taxes","الضرائب"),
        ("ppe_invesment","أصول ثابتة"),
        ("investment","استثمار"),
        ("loan","قروض"),
        ("asset_sale", "بيع أصول")
]

RECURSION = [
        ("daily", "يوميا"),
        ("weekly", "اسبوعيا"),
        ("monthly", "شهريا"),
        ("quarterly", "ربع سنوى"),
        ("semi-annual", "نصف سنوى"),
        ("annually", "سنويا")

]


# the business logic that handles
# entries and the amounts in the accounts
# def add_accounts(slug, amount):
#     # get the user
#     user_profile = get_object_or_404(UserMembership, user=request.user)
#     # get the account
#     account = get_object_or_404(Secondary, slug=slug)
#
#     # create an account item for the selected amount
#     account_item, _ = UserSecondary.objects.get_or_create(user_secondary_accounts=account)
#
#
#
#     if slug == "revenue":
#         revenue = UserSecondary.objects.filter(user_secondary_accounts.slug="revenue")
#         cash = UserSecondary.objects.filter(user_secondary_accounts.slug="cash")
#         if GeneralEntry.paid:
#             if GeneralEntry.made:
#                 revenue.update(amount+=amount)
#                 cash.update(amount+=amount)
#         else:
#             pass
