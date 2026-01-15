public interface IMicButton
{
    /// <summary>
    /// Evento quando l'utente preme il pulsante microfono.
    /// </summary>
    event System.Action OnMicPressed;

    /// <summary>
    /// Aggiorna lo stato visivo del pulsante.
    /// </summary>
    void SetListening(bool listening);
}
