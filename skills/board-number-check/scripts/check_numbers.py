#!/usr/bin/env python3
"""안건 숫자 점검 도구. 표준 라이브러리만 사용한다.

하위 명령
  sum      항목을 더해 기준값(기본: 승인 요청액)과 대조한다.
  ratio    비율(%)을 계산하고, 안건에 적힌 비율과 대조한다.
  diff     두 값의 차이를 계산한다(금리 차이 등). 단위가 %면 차이는 %p로 표시한다.
  payback  편익 실현율, 운영비, 대손비용에 따른 단순 회수기간을 계산한다.

테스트 예시 (가상 A은행 사례. 정답은 references/worked-example.md)
  python check_numbers.py sum --requested 150 개발=90 시스템연계=35 인프라=25 교육전환=15
  python check_numbers.py payback --investment 150 --benefit 45 --opex 12 --build-months 18

payback은 단순 민감도 예시다. 할인, 세금, 편익이 늘어나는 과정, 투자 지출 시점을
반영하지 않으므로 NPV나 경제성 승인의 근거로 쓰지 않는다.
"""
import argparse
import sys


def fmt(x):
    return f"{x:,.2f}".rstrip("0").rstrip(".")


def parse_item(text):
    name, sep, value = text.partition("=")
    if not sep or not name.strip():
        raise argparse.ArgumentTypeError(f"'이름=값' 형식이어야 합니다: {text}")
    try:
        return name.strip(), float(value.replace(",", ""))
    except ValueError:
        raise argparse.ArgumentTypeError(f"숫자가 아닙니다: {text}")


def cmd_sum(args):
    unit = args.unit
    label = args.label
    total = sum(v for _, v in args.items)
    print("[합계 점검]")
    for name, value in args.items:
        print(f"  {name:<12} {fmt(value):>10} {unit}")
    print(f"  {'합계':<12} {fmt(total):>10} {unit}")
    if args.requested is None:
        return 0
    diff = total - args.requested
    print(f"  {label:<10} {fmt(args.requested):>10} {unit}")
    if abs(diff) < 1e-9:
        print(f"  결과: 일치합니다(합계 = {label}).")
        return 0
    direction = "큽니다" if diff > 0 else "작습니다"
    print(f"  결과: 합계가 {label}보다 {fmt(abs(diff))} {unit} {direction}.")
    print("  주의: 원인(계산 오류, 중복 항목, 별도 예산, 부가세·예비비 포함 범위)은")
    print("        자료만으로 알 수 없습니다. 원인을 단정하지 말고 두 값을 맞춘")
    print("        조정표를 요청하십시오.")
    return 1


def cmd_ratio(args):
    if args.denominator == 0:
        print("[비율 점검]")
        print("  결과: 분모가 0이라 비율을 계산할 수 없습니다.")
        return 1
    pct = args.numerator / args.denominator * 100
    print("[비율 점검]")
    print(f"  분자  {fmt(args.numerator)}")
    print(f"  분모  {fmt(args.denominator)}")
    print(f"  결과: {pct:.2f}%")
    if args.stated is None:
        return 0
    diff = pct - args.stated
    print(f"  안건 기재값: {fmt(args.stated)}%")
    if abs(diff) <= args.tolerance:
        print(f"  대조: 반올림 범위(±{fmt(args.tolerance)}%p) 안에서 일치합니다.")
        return 0
    print(f"  대조: 안건 기재값과 {abs(diff):.2f}%p 차이가 납니다.")
    return 1


def cmd_diff(args):
    diff_unit = "%p" if args.unit == "%" else args.unit
    diff = args.value - args.base
    print("[차이 계산]")
    print(f"  {args.base_label:<12} {fmt(args.base):>10} {args.unit}")
    print(f"  {args.value_label:<12} {fmt(args.value):>10} {args.unit}")
    if abs(diff) < 1e-9:
        print("  결과: 두 값이 같습니다.")
        return 0
    sep = "" if diff_unit == "%p" else " "
    sign = "+" if diff > 0 else "−"
    bigger = args.value_label if diff > 0 else args.base_label
    print(f"  결과: {args.value_label} − {args.base_label} = {sign}{fmt(abs(diff))}{sep}{diff_unit} ({bigger} 쪽이 큼)")
    return 0


def to_rate(value):
    # 0.6과 60을 모두 받는다. 1 초과는 퍼센트로 본다.
    return value / 100 if value > 1 else value


def payback_row(investment, benefit, opex, credit_cost, rate, build_years):
    # 실현율은 총편익에만 적용하고, 운영비와 대손비용은 그대로 둔다.
    realized = benefit * rate
    net = realized - opex - credit_cost
    if net <= 0:
        return realized, net, None, None
    years = investment / net
    return realized, net, years, years + build_years


def cmd_payback(args):
    unit = args.unit
    build_years = args.build_months / 12
    rate = to_rate(args.realization)
    realized, net, years, with_build = payback_row(
        args.investment, args.benefit, args.opex, args.credit_cost, rate, build_years
    )

    print("[단순 회수기간 계산]")
    print(f"  투자금(전액 선투자 가정) {fmt(args.investment)} {unit}")
    print(f"  연간 기대 총편익         {fmt(args.benefit)} {unit}")
    print(f"  편익 실현율              {rate:.0%} (총편익에만 적용)")
    print(f"  연간 운영비              {fmt(args.opex)} {unit}")
    print(f"  연간 대손비용            {fmt(args.credit_cost)} {unit}")
    print(f"  구축 기간                {args.build_months:g}개월")
    print(f"  연간 실현 편익           {fmt(realized)} {unit}")
    print(f"  연간 순편익              {fmt(net)} {unit}")
    if years is None:
        print("  결과: 순편익이 0 이하라서 회수가 성립하지 않습니다.")
    else:
        print(f"  결과: 출시 후 약 {years:.2f}년")
        if args.build_months:
            print(f"        구축 기간을 더하면 약 {with_build:.2f}년")
    costs = args.opex + args.credit_cost
    if costs and args.benefit * rate > 0:
        wrong = args.investment / (args.benefit * rate)
        print(f"  참고: 운영비·대손비용을 빠뜨린 잘못된 계산은 {wrong:.2f}년으로 나옵니다.")

    if not args.no_sensitivity:
        print()
        print("[실현율 민감도] (실현율은 총편익에만 적용)")
        print(f"  {'실현율':>6} {'순편익':>10} {'출시 후 회수':>14} {'구축 포함':>12}")
        for r in (1.0, 0.8, 0.6, 0.4):
            _, n, y, yb = payback_row(
                args.investment, args.benefit, args.opex, args.credit_cost, r, build_years
            )
            if y is None:
                print(f"  {r:>6.0%} {fmt(n):>10} {'회수 불성립':>14} {'-':>12}")
            else:
                print(f"  {r:>6.0%} {fmt(n):>10} {y:>13.2f}년 {yb:>11.2f}년")

    print()
    print("주의: 할인, 세금, 편익이 늘어나는 과정, 투자 지출 시점을 반영하지 않은")
    print("      단순 민감도입니다. NPV나 경제성 승인의 근거로 쓰지 않습니다.")
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="안건 숫자 점검 도구")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("sum", help="항목 합계와 기준값 대조")
    p_sum.add_argument("items", nargs="+", type=parse_item, help="항목=금액 (여러 개)")
    p_sum.add_argument("--requested", type=float, help="대조할 기준값 (기본 의미: 승인 요청액)")
    p_sum.add_argument("--label", default="승인 요청액", help="기준값의 이름 (예: '표 기재 합계')")
    p_sum.add_argument("--unit", default="억 원", help="단위 (예: '백만 원')")
    p_sum.set_defaults(func=cmd_sum)

    # argparse help는 %-서식을 쓰므로 퍼센트 기호는 %%로 적는다.
    p_ratio = sub.add_parser("ratio", help="비율(%%) 계산과 안건 기재값 대조")
    p_ratio.add_argument("numerator", type=float, help="분자")
    p_ratio.add_argument("denominator", type=float, help="분모")
    p_ratio.add_argument("--stated", type=float, help="안건에 적힌 비율(%%)")
    p_ratio.add_argument("--tolerance", type=float, default=0.05, help="반올림 허용 범위(%%p)")
    p_ratio.set_defaults(func=cmd_ratio)

    p_diff = sub.add_parser("diff", help="두 값의 차이 (단위가 %%면 %%p로 표시)")
    p_diff.add_argument("base", type=float, help="기준값 (예: 안건 가정 금리)")
    p_diff.add_argument("value", type=float, help="비교값 (예: 현행 금리)")
    p_diff.add_argument("--unit", default="억 원", help="값의 단위 (예: '%%')")
    p_diff.add_argument("--base-label", default="기준값", help="기준값 이름")
    p_diff.add_argument("--value-label", default="비교값", help="비교값 이름")
    p_diff.set_defaults(func=cmd_diff)

    p_pb = sub.add_parser("payback", help="단순 회수기간과 실현율 민감도")
    p_pb.add_argument("--investment", type=float, required=True, help="투자금")
    p_pb.add_argument("--benefit", type=float, required=True, help="연간 기대 총편익 (운영비·대손비용 차감 전)")
    p_pb.add_argument("--opex", type=float, default=0.0, help="연간 운영비")
    p_pb.add_argument("--credit-cost", type=float, default=0.0, help="연간 대손비용")
    p_pb.add_argument("--realization", type=float, default=1.0, help="편익 실현율 (0.6 또는 60)")
    p_pb.add_argument("--build-months", type=float, default=0.0, help="구축 기간(개월)")
    p_pb.add_argument("--unit", default="억 원")
    p_pb.add_argument("--no-sensitivity", action="store_true", help="민감도 표 생략")
    p_pb.set_defaults(func=cmd_payback)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
