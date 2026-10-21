import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_diagram():
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Title
    ax.text(8, 9.6, 'SƠ ĐỒ KIẾN TRÚC TỔNG THỂ HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT MANAGEMENT)', 
            fontsize=16, fontweight='bold', ha='center', va='center', color='#0F172A', fontname='Arial')
    ax.text(8, 9.25, 'Đề 14: Sinh viên Đinh Gia Bảo - MSSV: DTC245220019 - Lớp ATTT K23A', 
            fontsize=11, ha='center', va='center', color='#475569', fontname='Arial')

    # Function to draw rounded boxes
    def draw_box(x, y, w, h, bg, border, title, desc, title_color='#0F172A'):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.3, title, fontsize=10, fontweight='bold', ha='center', va='top', color=title_color, fontname='Arial', zorder=3)
        if desc:
            ax.text(x + w/2, y + h - 0.65, desc, fontsize=8, ha='center', va='top', color='#334155', fontname='Arial', zorder=3, multialignment='center')

    # Function to draw group container
    def draw_group(x, y, w, h, bg, border, label):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor=bg, edgecolor=border, linewidth=1.8, linestyle='--', zorder=1)
        ax.add_patch(rect)
        ax.text(x + 0.3, y + h - 0.25, label, fontsize=9.5, fontweight='bold', color=border, fontname='Arial', zorder=3)

    # 1. CLIENT / BROWSER
    draw_box(0.5, 6.8, 2.2, 1.4, '#E0F2FE', '#0284C7', 'Client / Browser', 'Người dùng & Admin\nHTTPS: 8443\nHTTP: 8080 (301 Redirect)', '#0369A1')

    # 2. NETWORKS
    # Web Network Zone
    draw_group(3.3, 5.0, 7.8, 3.8, '#F0FDF4', '#16A34A', 'Docker Network: pm_web (Bridge)')

    # Database Network Zone (Internal)
    draw_group(11.5, 4.0, 4.2, 4.8, '#FEF2F2', '#DC2626', 'Docker Network: pm_database (Internal: True)')

    # Management Network Zone
    draw_group(7.5, 2.8, 3.6, 2.0, '#FFFBEB', '#D97706', 'Docker Network: pm_management')

    # Monitoring Network Zone
    draw_group(0.5, 0.4, 15.2, 2.2, '#F5F3FF', '#7C3AED', 'Docker Network: pm_monitoring (Bridge)')

    # 3. CONTAINERS
    # Nginx
    draw_box(3.6, 5.4, 3.2, 2.8, '#FFFFFF', '#16A34A', 'Nginx Reverse Proxy\n(pm-nginx)', 
             '• TLS 1.2 / 1.3 (RSA 3072)\n• Security Headers (HSTS, CSP)\n• Proxy pass -> pm-app:3000\n• Internal stub_status:8082\n• JSON Access / Error Logs', '#15803D')

    # App
    draw_box(7.5, 5.4, 3.2, 2.8, '#FFFFFF', '#2563EB', 'Node.js Express App\n(pm-app)', 
             '• Node 22 Alpine (Non-root)\n• EJS views, CSRF, Helmet\n• Readonly Rootfs + tmpfs\n• Least-privilege pg connection\n• JSON Structured Logging', '#1D4ED8')

    # PostgreSQL
    draw_box(11.8, 6.4, 3.6, 2.0, '#FFFFFF', '#DC2626', 'PostgreSQL 16 DB\n(pm-postgres)', 
             '• Port 5432 (Internal only)\n• Least privilege user: pm_app\n• Exporter user: postgres_exporter\n• Volume: pm_postgres_data', '#B91C1C')

    # pgAdmin
    draw_box(11.8, 4.3, 3.6, 1.8, '#FFFFFF', '#D97706', 'pgAdmin 4\n(pm-pgadmin)', 
             '• Web UI: 127.0.0.1:8081\n• Desktop mode (Auto-login)\n• Auto servers.json load\n• Volume: pm_pgadmin_data', '#B45309')

    # Monitoring Containers
    draw_box(0.8, 0.6, 2.6, 1.6, '#FFFFFF', '#7C3AED', 'Prometheus v3.2.1\n(pm-prometheus)', '• Scrape interval: 15s\n• Retention: 7 days\n• Port: 127.0.0.1:9090\n• 4 Targets UP (100%)', '#6D28D9')
    draw_box(3.7, 0.6, 2.6, 1.6, '#FFFFFF', '#7C3AED', 'Grafana v11.5.0\n(pm-grafana)', '• UI: 127.0.0.1:3002\n• Auto Datasources (Prom/Loki)\n• Dashboard Containers/Web/DB\n• Port 3002 (Tránh xung đột)', '#6D28D9')
    draw_box(6.6, 0.6, 2.6, 1.6, '#FFFFFF', '#7C3AED', 'cAdvisor\n(pm-cadvisor)', '• Host daemon metrics\n• CPU, RAM, Disk, Net\n• Internal port: 8080', '#6D28D9')
    draw_box(9.5, 0.6, 2.6, 1.6, '#FFFFFF', '#7C3AED', 'Exporters\n(Nginx + Postgres)', '• nginx-exporter:9113\n• postgres-exporter:9187\n• Scrape stub_status & stats', '#6D28D9')
    draw_box(12.4, 0.6, 3.0, 1.6, '#FFFFFF', '#7C3AED', 'Loki + Promtail v3.4.2\n(pm-loki & pm-promtail)', '• Promtail: mount read-only log\n• Loki: TSDB v13 storage (3100)\n• LogQL queries cho audit/error', '#6D28D9')

    # Arrows
    def draw_arrow(x1, y1, x2, y2, label='', color='#475569'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, shrinkA=3, shrinkB=3), zorder=4)
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, fontsize=7.5, fontweight='bold', ha='center', va='bottom', color=color, fontname='Arial', zorder=5)

    # Client -> Nginx
    draw_arrow(2.7, 7.5, 3.6, 7.5, 'HTTPS:8443', '#0284C7')

    # Nginx -> App
    draw_arrow(6.8, 6.8, 7.5, 6.8, 'proxy_pass :3000', '#16A34A')

    # App -> Postgres
    draw_arrow(10.7, 7.4, 11.8, 7.4, 'pg pool :5432', '#DC2626')

    # pgAdmin -> Postgres
    draw_arrow(13.6, 5.8, 13.6, 6.4, 'admin connect', '#D97706')

    # Promtail -> App Logs & Nginx Logs
    draw_arrow(13.9, 2.2, 10.7, 5.8, 'tail logs (ro)', '#7C3AED')
    draw_arrow(13.9, 2.2, 5.2, 5.4, 'tail access.log (ro)', '#7C3AED')

    # Exporters -> Services
    draw_arrow(10.8, 2.2, 5.2, 5.4, 'stub_status :8082', '#059669')
    draw_arrow(10.8, 2.2, 13.0, 6.4, 'pg_monitor :5432', '#DC2626')

    # Prometheus -> Targets
    draw_arrow(2.1, 2.2, 4.0, 2.2, 'scrape', '#7C3AED')
    draw_arrow(2.1, 2.2, 7.0, 2.2, 'scrape', '#7C3AED')
    draw_arrow(2.1, 2.2, 10.0, 2.2, 'scrape', '#7C3AED')

    # Grafana -> Prom & Loki
    draw_arrow(3.7, 1.4, 3.4, 1.4, 'PromQL', '#6D28D9')
    draw_arrow(6.3, 1.4, 12.4, 1.4, 'LogQL', '#6D28D9')

    plt.tight_layout()
    plt.savefig('docs/evidence/00_architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('Generated architecture diagram: docs/evidence/00_architecture_diagram.png')

if __name__ == '__main__':
    create_diagram()
