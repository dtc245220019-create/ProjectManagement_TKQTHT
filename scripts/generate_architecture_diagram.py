import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_diagram():
    fig, ax = plt.subplots(figsize=(13, 8.2), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Main Title
    ax.text(6.5, 7.82, 'ĐỀ 14: KIẾN TRÚC TRIỂN KHAI HỆ THỐNG QUẢN LÝ DỰ ÁN THỰC TẾ',
            fontsize=13.5, fontweight='bold', ha='center', va='center', color='#1E293B', fontname='Times New Roman')

    def draw_node(x, y, w, h, title, line1, line2, bg='#F8FAFC', border='#475569'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.4, zorder=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.26, title, fontsize=11, fontweight='bold',
                ha='center', va='center', color='#0F172A', fontname='Arial', zorder=3)
        ax.text(x + w/2, y + h/2 - 0.04, line1, fontsize=9,
                ha='center', va='center', color='#334155', fontname='Arial', zorder=3)
        ax.text(x + w/2, y + 0.22, line2, fontsize=9,
                ha='center', va='center', color='#475569', fontname='Arial', zorder=3)

    # Grid coordinates
    w = 2.5
    h = 1.25
    cols = [0.5, 3.6, 6.9, 10.0]
    y_row1 = 5.9
    y_row2 = 3.85
    y_row3 = 1.8

    # ROW 1: User Request & Core App Flow
    draw_node(cols[0], y_row1, w, h, 'Trình duyệt', 'HTTP 8080 (Redirect 301)', 'HTTPS 8443 (TLS 1.2/1.3)', '#F8FAFC', '#334155')
    draw_node(cols[1], y_row1, w, h, 'Nginx non-root', 'Reverse proxy (UID 101)', 'Security headers & TLS', '#F0FDF4', '#15803D')
    draw_node(cols[2], y_row1, w, h, 'Express và EJS', 'Quản lý Dự án, Task, Member', 'Cổng nội bộ 3000 (UID 1000)', '#EFF6FF', '#1D4ED8')
    draw_node(cols[3], y_row1, w, h, 'PostgreSQL 16', 'pm_db · 7 bảng dữ liệu', 'Không publish cổng DB', '#FEF2F2', '#B91C1C')

    # ROW 2: Exporters, Volumes log, pgAdmin 4
    draw_node(cols[1], y_row2, w, h, 'Exporters', 'Nginx và Postgres Exporters', 'cAdvisor container metrics', '#F5F3FF', '#6D28D9')
    draw_node(cols[2], y_row2, w, h, 'Volumes log', 'Nginx access/error JSON', 'App JSON log (app.log)', '#FFFBEB', '#B45309')
    draw_node(cols[3], y_row2, w, h, 'pgAdmin 4', '127.0.0.1:8081 (Desktop)', 'Quản trị CSDL PostgreSQL', '#FEF2F2', '#B91C1C')

    # ROW 3: Observability & Logging Stack
    draw_node(cols[0], y_row3, w, h, 'Grafana', '127.0.0.1:3002', 'Dashboard và Explore', '#F5F3FF', '#6D28D9')
    draw_node(cols[1], y_row3, w, h, 'Prometheus', '127.0.0.1:9090', 'Scrape mỗi 15 giây', '#F5F3FF', '#6D28D9')
    draw_node(cols[2], y_row3, w, h, 'Promtail', 'Đọc volumes :ro', 'Gắn nhãn job=app/nginx', '#FFFBEB', '#B45309')
    draw_node(cols[3], y_row3, w, h, 'Loki', 'TSDB v13 và filesystem', 'Retention 7 ngày (168h)', '#FFFBEB', '#B45309')

    def draw_arrow(x1, y1, x2, y2, label='', lx=None, ly=None):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#334155', lw=1.4, shrinkA=2, shrinkB=2), zorder=4)
        if label:
            tx = lx if lx is not None else (x1 + x2) / 2
            ty = ly if ly is not None else (y1 + y2) / 2 + 0.12
            ax.text(tx, ty, label, fontsize=8.5, ha='center', va='center', color='#334155', fontname='Arial',
                    bbox=dict(facecolor='#FFFFFF', edgecolor='none', pad=1.8), zorder=5)

    # Horizontal arrows Row 1
    draw_arrow(cols[0] + w, y_row1 + h/2, cols[1], y_row1 + h/2, 'request')
    draw_arrow(cols[1] + w, y_row1 + h/2, cols[2], y_row1 + h/2, 'proxy')
    draw_arrow(cols[2] + w, y_row1 + h/2, cols[3], y_row1 + h/2, 'SQL')

    # Vertical / Diagonal arrows Row 1 -> Row 2
    draw_arrow(cols[1] + w*0.75, y_row1, cols[2] + w*0.25, y_row2 + h, 'ghi file',
               lx=(cols[1] + w*0.75 + cols[2] + w*0.25)/2 - 0.15, ly=(y_row1 + y_row2 + h)/2)
    draw_arrow(cols[2] + w/2, y_row1, cols[2] + w/2, y_row2 + h, 'ghi file',
               lx=cols[2] + w/2 + 0.35, ly=(y_row1 + y_row2 + h)/2)
    draw_arrow(cols[3] + w/2, y_row2 + h, cols[3] + w/2, y_row1, 'mạng database',
               lx=cols[3] + w/2, ly=(y_row1 + y_row2 + h)/2)

    # Vertical arrows Row 2 <-> Row 3
    draw_arrow(cols[1] + w/2, y_row3 + h, cols[1] + w/2, y_row2, 'metrics',
               lx=cols[1] + w/2, ly=(y_row2 + y_row3 + h)/2)
    draw_arrow(cols[2] + w/2, y_row2, cols[2] + w/2, y_row3 + h, 'thu gom',
               lx=cols[2] + w/2, ly=(y_row2 + y_row3 + h)/2)

    # Horizontal arrows Row 3
    draw_arrow(cols[0] + w, y_row3 + h/2, cols[1], y_row3 + h/2, 'PromQL')
    draw_arrow(cols[2] + w, y_row3 + h/2, cols[3], y_row3 + h/2, 'push log')

    # Bottom U-line connecting Grafana to Loki
    gx = cols[0] + w/2
    lx = cols[3] + w/2
    by = 1.15
    ax.plot([gx, gx, lx, lx], [y_row3, by, by, y_row3], color='#334155', lw=1.3, zorder=3)
    ax.text((gx + lx)/2, by + 0.16, 'Grafana truy vấn Loki bằng LogQL qua mạng monitoring',
            fontsize=9, ha='center', va='center', color='#334155', fontname='Arial')

    # Bottom Network Pill
    pill = patches.FancyBboxPatch((3.1, 0.45), 6.8, 0.35, boxstyle="round,pad=0.05,rounding_size=0.15",
                                  facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1.0, zorder=2)
    ax.add_patch(pill)
    ax.text(6.5, 0.62, 'Mạng pm_web · pm_database (internal) · pm_management · pm_monitoring',
            fontsize=9, fontweight='bold', ha='center', va='center', color='#1E293B', fontname='Arial')

    ax.text(6.5, 0.18, 'Nguồn sơ đồ: compose.yaml, compose.monitoring.yaml và compose.logging.yaml',
            fontsize=8.5, style='italic', ha='center', va='center', color='#475569', fontname='Times New Roman')

    plt.tight_layout()
    plt.savefig('docs/evidence/00_architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Successfully generated clean architecture diagram!')

if __name__ == '__main__':
    create_diagram()
