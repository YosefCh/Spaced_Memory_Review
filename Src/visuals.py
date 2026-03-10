"""
visuals.py
==========
All learning-dashboard visuals. Each function loads the CSV independently
and displays its chart. Call run_all() to render every visual at once.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import seaborn as sns

CSV_PATH = r'C:\Users\Rebecca\OneDrive\Documents\Review\Data\learned_material.csv'


# ─────────────────────────────────────────────
# 1. Entries per Subject (Horizontal Bar Chart)
# ─────────────────────────────────────────────
def plot_subject_bar(threshold=2):
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=['Subject'])
    subject_counts = df['Subject'].value_counts()
    other_count = subject_counts[subject_counts < threshold].sum()
    grouped = subject_counts[subject_counts >= threshold].copy()
    if other_count > 0:
        grouped['Other'] = other_count

    subject_df = grouped.reset_index()
    subject_df.columns = ['Subject', 'Count']
    subject_sorted = subject_df.sort_values('Count', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    sns.barplot(
        data=subject_sorted, x='Count', y='Subject',
        hue='Subject', dodge=False, legend=False, palette='viridis'
    )
    plt.title('Number of Learned Items per Subject (Grouped)')
    plt.xlabel('Count', labelpad=12, fontweight='bold', color="#011614")
    plt.ylabel('Subject', labelpad=18, fontweight='bold', color="#02022A")
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# 2. Weekly Learning Consistency (Line Chart)
# ─────────────────────────────────────────────
def plot_weekly_consistency(goal=4):
    df = pd.read_csv(CSV_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = df['Date'].min().normalize()
    end_date = pd.Timestamp.today().normalize()
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    daily = (
        df.assign(activity_valid=df['Subject'].notna())
        .groupby(df['Date'].dt.date)['activity_valid']
        .any().astype(int).rename('learned_flag').reset_index()
    )
    daily['Date'] = pd.to_datetime(daily['Date'])

    full_range = pd.date_range(start=start_date, end=end_date, freq='D')
    daily_full = (
        daily.set_index('Date')[['learned_flag']]
        .reindex(full_range).fillna(0).astype(int)
    )
    daily_full.index.name = 'Date'
    daily_full = daily_full.reset_index()
    daily_full['days_from_start'] = (daily_full['Date'] - start_date).dt.days
    daily_full['week_index'] = daily_full['days_from_start'] // 7

    weekly = (
        daily_full.groupby('week_index')['learned_flag']
        .sum().reset_index()
    )
    weekly['week_start'] = start_date + pd.to_timedelta(weekly['week_index'] * 7, unit='D')

    plt.figure(figsize=(12, 6))
    sns.set_theme(style='whitegrid')
    sns.lineplot(data=weekly, x='week_start', y='learned_flag', marker='o', color='#1f77b4')
    plt.ylim(0, 7)
    plt.yticks(range(0, 8))
    plt.title('Weekly Learning Consistency (Days with Learning per 7-Day Block)', fontsize=14, fontweight='bold')
    plt.xlabel('Week Starting', labelpad=10)
    plt.ylabel('Days with Learning (0–7)', labelpad=10)
    plt.axhline(7, color='green', linestyle='--', linewidth=1, label='Perfect Week (7/7)')
    plt.axhline(goal, color='orange', linestyle='--', linewidth=1, label=f'Goal ({goal} days)')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# 3. Gap Analysis (Days Since Last Studied)
# ─────────────────────────────────────────────
def plot_gap_analysis(yellow_threshold=150, red_threshold=300):
    df = pd.read_csv(CSV_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    today = pd.Timestamp.today().normalize()

    last_studied = df.groupby('Subject')['Date'].max().reset_index()
    last_studied['days_since'] = (today - last_studied['Date']).dt.days
    last_studied = last_studied.sort_values('days_since', ascending=True)

    colors = [
        '#d73027' if d > red_threshold else '#fee08b' if d > yellow_threshold else '#1a9850'
        for d in last_studied['days_since']
    ]

    fig, ax = plt.subplots(figsize=(10, max(6, len(last_studied) * 0.38)))
    bars = ax.barh(last_studied['Subject'], last_studied['days_since'], color=colors)
    for bar, val in zip(bars, last_studied['days_since']):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                f'{val}d', va='center', fontsize=9)

    ax.axvline(yellow_threshold, color='#f59e0b', linestyle='--', linewidth=1.3,
               label=f'{yellow_threshold} days (yellow zone)')
    ax.axvline(red_threshold, color='#ef4444', linestyle='--', linewidth=1.3,
               label=f'{red_threshold} days (red zone)')
    ax.set_xlabel('Days Since Last Studied', fontweight='bold', labelpad=10)
    ax.set_title('Gap Analysis: Days Since Each Subject Was Last Studied', fontsize=13, fontweight='bold')
    ax.legend(loc='lower right')
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# 4. Pie Chart: Learning Days vs. Empty Days
# ─────────────────────────────────────────────
def plot_learning_pie(start_date=None, end_date=None):
    """
    start_date / end_date: datetime.date objects (or None to use data min / today).
    """
    df = pd.read_csv(CSV_PATH)
    df['Date'] = pd.to_datetime(df['Date'])

    data_start = df['Date'].min().normalize()
    data_end   = pd.Timestamp.today().normalize()

    start = pd.Timestamp(start_date).normalize() if start_date else data_start
    end   = pd.Timestamp(end_date).normalize()   if end_date   else data_end

    # Guard against inverted range
    if start > end:
        print("Start date must be before end date.")
        return

    total_days = (end - start).days + 1
    df = df[(df['Date'] >= start) & (df['Date'] <= end)]

    active_days = (
        df.groupby(df['Date'].dt.normalize())
        .apply(lambda g: g['Subject'].notna().any() or g['Topic'].notna().any())
        .sum()
    )
    empty_days = total_days - active_days

    period_label = f"{start.strftime('%b %d %Y')}  →  {end.strftime('%b %d %Y')}"

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        [active_days, empty_days],
        labels=[f'Days Learned\n({active_days})', f'Empty Days\n({empty_days})'],
        colors=['#30a14e', '#9d9fa2'],
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(edgecolor='white', linewidth=2),
        textprops=dict(fontsize=12)
    )
    ax.set_title(f'Learning Days vs. Empty Days\n({period_label})',
                 fontsize=13, fontweight='bold', pad=16)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# Run all visuals
# ─────────────────────────────────────────────
def run_all():
    plot_subject_bar()
    plot_weekly_consistency()
    plot_gap_analysis()
    plot_learning_pie()


if __name__ == '__main__':
    run_all()
