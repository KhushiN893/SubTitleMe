# imports.py
import os
import subprocess
import soundfile as sf
import librosa
from transformers import pipeline
from flask import Flask, request, render_template
import requests