import subprocess
import json
import os

if __name__ == '__main__':
    def sh(cmd):
        p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return p.stdout.strip()

    app_id = sh('docker exec pm-app id')
    inspect_app = json.loads(sh('docker inspect pm-app'))[0]
    inspect_db_net = json.loads(sh('docker network inspect pm_database_network'))[0]
    inspect_pg = json.loads(sh('docker inspect pm-postgres'))[0]
    grants = sh("docker exec pm-postgres psql -U postgres -d pm_db -c \"SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE grantee = 'pm_app' AND table_name = 'projects';\"")

    evidence = {
        'app_uid': app_id,
        'readonly_rootfs': inspect_app['HostConfig']['ReadonlyRootfs'],
        'cap_drop': inspect_app['HostConfig']['CapDrop'],
        'security_opt': inspect_app['HostConfig']['SecurityOpt'],
        'tmpfs': inspect_app['HostConfig']['Tmpfs'],
        'database_network_internal': inspect_db_net['Internal'],
        'postgres_port_bindings': inspect_pg['HostConfig']['PortBindings'],
        'pm_app_table_grants': grants
    }

    os.makedirs('docs/evidence', exist_ok=True)
    with open('docs/evidence/hardening_verification.json', 'w', encoding='utf-8') as f:
        json.dump(evidence, f, indent=2, ensure_ascii=False)

    print('[+] Hardening verification collected successfully:')
    print(json.dumps(evidence, indent=2, ensure_ascii=False))
