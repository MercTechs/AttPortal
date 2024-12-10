-- Clear existing data if needed
TRUNCATE TABLE attendance_records CASCADE;

-- Insert mock attendance records
INSERT INTO attendance_records (
    uuid,
    employee_id,
    employee_name,
    machine_alias,
    machine_serial,
    att_date,
    check_time,
    attendance_status,
    sync_status,
    created_at
) VALUES
    ('11111111-1111-1111-1111-111111111101', '00210', 'Employee 210', 'MC4732', 'AYSB28014732', '2024-12-02', '2024-12-02 07:52:34', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111102', '00210', 'Employee 210', 'MC4698', 'AYSB28014698', '2024-12-02', '2024-12-02 07:06:57', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111103', '00210', 'Employee 210', 'MC4732', 'AYSB28014732', '2024-12-03', '2024-12-03 07:47:28', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111104', '00210', 'Employee 210', 'MC4698', 'AYSB28014698', '2024-12-03', '2024-12-03 07:18:20', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111105', '00210', 'Employee 210', 'MC4732', 'AYSB28014732', '2024-12-04', '2024-12-04 07:50:02', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111106', '00210', 'Employee 210', 'MC4698', 'AYSB28014698', '2024-12-04', '2024-12-04 07:15:40', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111107', '00210', 'Employee 210', 'MC4732', 'AYSB28014732', '2024-12-05', '2024-12-05 08:23:23', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111108', '00210', 'Employee 210', 'MC4698', 'AYSB28014698', '2024-12-05', '2024-12-05 07:01:03', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111109', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-02', '2024-12-02 07:52:28', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111110', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-02', '2024-12-02 07:28:58', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111111', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-03', '2024-12-03 08:24:32', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111112', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-03', '2024-12-03 07:00:11', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111113', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-04', '2024-12-04 08:11:44', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111114', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-04', '2024-12-04 07:08:22', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111115', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-05', '2024-12-05 07:55:31', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111116', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-05', '2024-12-05 07:04:28', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111117', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-06', '2024-12-06 07:52:28', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111118', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-06', '2024-12-06 07:28:58', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111119', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-09', '2024-12-09 08:24:32', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111120', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-09', '2024-12-09 07:00:11', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111121', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-10', '2024-12-10 08:11:44', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111122', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-10', '2024-12-10 07:08:22', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111123', '00211', 'Employee 211', 'MC4732', 'AYSB28014732', '2024-12-11', '2024-12-11 07:55:31', 'None', 'synced', NOW()),
    ('11111111-1111-1111-1111-111111111124', '00211', 'Employee 211', 'MC4698', 'AYSB28014698', '2024-12-11', '2024-12-11 07:04:28', 'None', 'synced', NOW());

-- Insert mock devices with their types
INSERT INTO attendance_devices (
    uuid,
    device_id,
    serial_number,
    name,
    device_type,
    sync_status,
    is_active,
    last_sync
) VALUES
    ('22222222-2222-2222-2222-222222222201', 'DEV4732', 'AYSB28014732', 'Device 4732', 'CHECK_IN', 'ACTIVE', true, NOW()),
    ('22222222-2222-2222-2222-222222222202', 'DEV4698', 'AYSB28014698', 'Device 4698', 'CHECK_OUT', 'ACTIVE', true, NOW())
ON CONFLICT (serial_number) DO UPDATE 
SET device_type = EXCLUDED.device_type,
    last_sync = NOW();
