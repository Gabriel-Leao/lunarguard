import cv2
import mediapipe as mp
import time


# Paleta temática espacial
COLOR_OK         = (0, 220, 80)      # verde
COLOR_WARN       = (0, 200, 255)     # amarelo
COLOR_ALERT      = (0, 50, 220)      # vermelho
COLOR_ZONE_FREE  = (80, 200, 80)     # verde translúcido
COLOR_ZONE_RESTR = (0, 60, 200)      # vermelho translúcido
COLOR_MOTION     = (0, 200, 255)     # amarelo
COLOR_TEXT_BG    = (15, 15, 15)
COLOR_WHITE      = (230, 230, 230)
COLOR_CYAN       = (200, 220, 0)


class Overlay:
    def __init__(self):
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_pose    = mp.solutions.pose
        self._alert_until = 0.0          # timestamp até quando exibir alerta
        self._alert_msg   = ""

    # ------------------------------------------------------------------ #
    #  ZONAS
    # ------------------------------------------------------------------ #
    def draw_zones(self, frame, zones):
        overlay = frame.copy()
        for zone in zones:
            color = COLOR_ZONE_RESTR if zone.restricted else COLOR_ZONE_FREE
            cv2.rectangle(overlay, (zone.x1, zone.y1), (zone.x2, zone.y2), color, -1)
            cv2.rectangle(frame,   (zone.x1, zone.y1), (zone.x2, zone.y2), color,  2)

            label = f"[RESTRITO] {zone.name}" if zone.restricted else zone.name
            cv2.putText(
                frame, label,
                (zone.x1 + 6, zone.y1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, color, 1, cv2.LINE_AA,
            )

        cv2.addWeighted(overlay, 0.12, frame, 0.88, 0, frame)

    # ------------------------------------------------------------------ #
    #  MOVIMENTO
    # ------------------------------------------------------------------ #
    def draw_motion_boxes(self, frame, boxes):
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR_MOTION, 2)
            cv2.putText(
                frame, "MOV",
                (x + 4, y - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_MOTION, 1, cv2.LINE_AA,
            )

    # ------------------------------------------------------------------ #
    #  POSE / ESQUELETO
    # ------------------------------------------------------------------ #
    def draw_pose(self, frame, landmarks):
        if landmarks is None:
            return
        self._mp_drawing.draw_landmarks(
            frame,
            landmarks,
            self._mp_pose.POSE_CONNECTIONS,
            self._mp_drawing.DrawingSpec(color=COLOR_CYAN, thickness=2, circle_radius=3),
            self._mp_drawing.DrawingSpec(color=COLOR_WHITE, thickness=1),
        )

    # ------------------------------------------------------------------ #
    #  ALERTAS
    # ------------------------------------------------------------------ #
    def trigger_alert(self, message: str, duration: float = 2.5):
        self._alert_until = time.time() + duration
        self._alert_msg   = message

    def draw_alert(self, frame):
        if time.time() > self._alert_until:
            return
        h, w = frame.shape[:2]
        # Barra de alerta
        cv2.rectangle(frame, (0, h - 60), (w, h), COLOR_ALERT, -1)
        cv2.putText(
            frame,
            f"⚠  ALERTA: {self._alert_msg}",
            (16, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_WHITE, 2, cv2.LINE_AA,
        )
        # Borda piscante
        t = int(time.time() * 4) % 2
        if t:
            cv2.rectangle(frame, (0, 0), (w - 1, h - 1), COLOR_ALERT, 4)

    # ------------------------------------------------------------------ #
    #  HUD SUPERIOR
    # ------------------------------------------------------------------ #
    def draw_hud(self, frame, status: str, fps: float, fall: bool, intrusion: bool):
        h, w = frame.shape[:2]

        # Barra superior
        cv2.rectangle(frame, (0, 0), (w, 38), COLOR_TEXT_BG, -1)

        # Status geral
        if fall or intrusion:
            s_color, s_text = COLOR_ALERT, "STATUS: ALERTA"
        else:
            s_color, s_text = COLOR_OK, "STATUS: NOMINAL"

        cv2.putText(frame, "LUNARGUARD v1.0", (10, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_CYAN, 2, cv2.LINE_AA)
        cv2.putText(frame, s_text, (w // 2 - 100, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, s_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"FPS: {fps:.1f}", (w - 110, 26),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_WHITE, 1, cv2.LINE_AA)

        # Indicadores laterais
        fall_color = COLOR_ALERT if fall else COLOR_OK
        intr_color = COLOR_ALERT if intrusion else COLOR_OK
        cv2.putText(frame, f"QUEDA: {'SIM' if fall else 'NAO'}",
                    (10, h - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.55, fall_color, 2, cv2.LINE_AA)
        cv2.putText(frame, f"INTRUSAO: {'SIM' if intrusion else 'NAO'}",
                    (10, h - 48), cv2.FONT_HERSHEY_SIMPLEX, 0.55, intr_color, 2, cv2.LINE_AA)
