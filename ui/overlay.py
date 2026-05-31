import cv2
import time


COLOR_OK         = (0, 220, 80)
COLOR_ALERT      = (0, 50, 220)
COLOR_ZONE_RESTR = (0, 60, 200)
COLOR_MOTION     = (0, 200, 255)
COLOR_TEXT_BG    = (15, 15, 15)
COLOR_WHITE      = (230, 230, 230)
COLOR_CYAN       = (200, 220, 0)


class Overlay:
    def __init__(self):
        self._alert_until = 0.0
        self._alert_msg = ""

    def draw_zones(self, frame, zones):
        overlay = frame.copy()
        for zone in zones:
            cv2.rectangle(overlay, (zone.x1, zone.y1), (zone.x2, zone.y2), COLOR_ZONE_RESTR, -1)
            cv2.rectangle(frame, (zone.x1, zone.y1), (zone.x2, zone.y2), COLOR_ZONE_RESTR, 2)
            cv2.putText(frame, f"[R] {zone.name}", (zone.x1 + 4, zone.y1 + 16),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, COLOR_ZONE_RESTR, 1, cv2.LINE_AA)
        cv2.addWeighted(overlay, 0.18, frame, 0.82, 0, frame)

    def draw_motion_boxes(self, frame, boxes):
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR_MOTION, 2)
            cv2.putText(frame, "MOV", (x + 4, y - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_MOTION, 1, cv2.LINE_AA)

    def draw_pose(self, frame, landmarks):
        if landmarks is None:
            return
        h, w = frame.shape[:2]
        from detector.pose import POSE_CONNECTIONS
        for lm in landmarks:
            cv2.circle(frame, (int(lm.x * w), int(lm.y * h)), 4, COLOR_CYAN, -1)
        for s, e in POSE_CONNECTIONS:
            if s >= len(landmarks) or e >= len(landmarks):
                continue
            cv2.line(frame,
                     (int(landmarks[s].x * w), int(landmarks[s].y * h)),
                     (int(landmarks[e].x * w), int(landmarks[e].y * h)),
                     COLOR_WHITE, 1, cv2.LINE_AA)

    def draw_face(self, frame, face_landmarks):
        if face_landmarks is None:
            return
        h, w = frame.shape[:2]
        from detector.blink import _LEFT_EYE, _RIGHT_EYE
        for indices in (_LEFT_EYE, _RIGHT_EYE):
            pts = [(int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)) for i in indices]
            for j in range(len(pts)):
                cv2.line(frame, pts[j], pts[(j + 1) % len(pts)], COLOR_CYAN, 1, cv2.LINE_AA)

    def trigger_alert(self, message: str, duration: float = 2.5):
        self._alert_until = time.time() + duration
        self._alert_msg = message

    def draw_alert(self, frame):
        if time.time() > self._alert_until:
            return
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, h - 60), (w, h), COLOR_ALERT, -1)
        cv2.putText(frame, f"ALERTA: {self._alert_msg}", (16, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_WHITE, 2, cv2.LINE_AA)
        if int(time.time() * 4) % 2:
            cv2.rectangle(frame, (0, 0), (w - 1, h - 1), COLOR_ALERT, 4)

    def draw_legend(self, frame):
        h, w = frame.shape[:2]
        keys = [
            ("[Z] Ocultar HUD",   COLOR_CYAN),
            ("[R] Resetar fundo", COLOR_WHITE),
            ("[Q] Sair",          COLOR_WHITE),
        ]
        padding = 10
        line_h  = 28
        box_h   = padding * 2 + len(keys) * line_h
        box_w   = 220
        x0      = w - box_w - 10
        y0      = 48

        bg = frame.copy()
        cv2.rectangle(bg, (x0, y0), (x0 + box_w, y0 + box_h), COLOR_TEXT_BG, -1)
        cv2.addWeighted(bg, 0.6, frame, 0.4, 0, frame)
        cv2.rectangle(frame, (x0, y0), (x0 + box_w, y0 + box_h), COLOR_CYAN, 1)

        for i, (text, color) in enumerate(keys):
            cv2.putText(frame, text,
                        (x0 + padding, y0 + padding + (i + 1) * line_h - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.58, color, 1, cv2.LINE_AA)

    def draw_hud(self, frame, fps: float, fall: bool, intrusion: bool, eyes_closed: bool):
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (0, 0), (w, 38), COLOR_TEXT_BG, -1)

        alert = fall or intrusion or eyes_closed
        s_color = COLOR_ALERT if alert else COLOR_OK
        s_text  = "STATUS: ALERTA" if alert else "STATUS: NOMINAL"

        cv2.putText(frame, "LUNARGUARD v1.0", (10, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_CYAN, 2, cv2.LINE_AA)
        cv2.putText(frame, s_text, (w // 2 - 100, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, s_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"FPS: {fps:.1f}", (w - 110, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_WHITE, 1, cv2.LINE_AA)

        indicators = [
            (f"QUEDA:       {'SIM' if fall        else 'NAO'}", fall),
            (f"INTRUSAO:    {'SIM' if intrusion   else 'NAO'}", intrusion),
            (f"OLHOS FECH.: {'SIM' if eyes_closed else 'NAO'}", eyes_closed),
        ]
        for i, (text, active) in enumerate(indicators):
            color = COLOR_ALERT if active else COLOR_OK
            cv2.putText(frame, text, (10, h - 100 + i * 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.68, color, 2, cv2.LINE_AA)
