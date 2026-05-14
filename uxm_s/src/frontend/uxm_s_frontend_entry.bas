#ifndef UXM_S_FRONTEND_ENTRY_BAS
#define UXM_S_FRONTEND_ENTRY_BAS

#Include Once "address_resolver/uxm_v20_addressing_modes.bas"

Type UXSFrontendToken
    kind As Long
    text As String
    lineNo As Long
    colNo As Long
End Type

Const UXS_TOK_EOF As Long = 0
Const UXS_TOK_SYMBOL As Long = 1
Const UXS_TOK_NUMBER As Long = 2
Const UXS_TOK_IDENT As Long = 3
Const UXS_TOK_STRING As Long = 4
Const UXS_TOK_META As Long = 5
Const UXS_TOK_PRAGMA As Long = 6

Type UXSFrontendStats
    tokenCount As Long
    astNodeCount As Long
    addressValidCount As Long
    addressInvalidCount As Long
    metaCount As Long
    stringCount As Long
    commandCount As Long
End Type

Dim Shared g_uxsLastError As String
Dim Shared g_uxsLastStats As UXSFrontendStats
Dim Shared g_uxsTokens() As UXSFrontendToken
Dim Shared g_uxsTokenCount As Long
Dim Shared g_uxsLexError As String

Function UXS_IsDigit(ByVal ch As String) As Long
    Return IIf(ch >= "0" And ch <= "9", -1, 0)
End Function

Function UXS_IsIdent(ByVal ch As String) As Long
    Return IIf((ch >= "a" And ch <= "z") Or (ch >= "A" And ch <= "Z") Or UXS_IsDigit(ch) Or ch = "_", -1, 0)
End Function

Sub UXS_AddToken(ByVal kind As Long, ByVal txt As String, ByVal lineNo As Long, ByVal colNo As Long)
    g_uxsTokenCount += 1
    If g_uxsTokenCount > UBound(g_uxsTokens) Then
        ReDim Preserve g_uxsTokens(0 To UBound(g_uxsTokens) + 256) As UXSFrontendToken
    End If
    g_uxsTokens(g_uxsTokenCount).kind = kind
    g_uxsTokens(g_uxsTokenCount).text = txt
    g_uxsTokens(g_uxsTokenCount).lineNo = lineNo
    g_uxsTokens(g_uxsTokenCount).colNo = colNo
End Sub

Sub UXS_Lex(ByVal sourceText As String)
    Dim p As Long = 1
    Dim ln As Long = 1
    Dim co As Long = 1
    ReDim g_uxsTokens(0 To 255) As UXSFrontendToken
    g_uxsTokenCount = 0
    g_uxsLexError = ""

    While p <= Len(sourceText)
        Dim ch As String = Mid(sourceText, p, 1)
        Dim startP As Long = p
        Dim startC As Long = co

        If ch = Chr(10) Then
            p += 1
            ln += 1
            co = 1
            Continue While
        End If

        If ch = " " Or ch = Chr(9) Or ch = Chr(13) Then
            p += 1
            co += 1
            Continue While
        End If

        If ch = "'" Then
            While p <= Len(sourceText) And Mid(sourceText, p, 1) <> Chr(10)
                p += 1
                co += 1
            Wend
            Continue While
        End If

        If ch = "#" Then
            While p <= Len(sourceText) And Mid(sourceText, p, 1) <> Chr(10)
                p += 1
                co += 1
            Wend
            UXS_AddToken UXS_TOK_PRAGMA, Mid(sourceText, startP, p - startP), ln, startC
            Continue While
        End If

        If ch = "@" Then
            p += 1
            co += 1
            If p <= Len(sourceText) And Mid(sourceText, p, 1) = "!" Then
                p += 1
                co += 1
            End If
            If p <= Len(sourceText) And Mid(sourceText, p, 1) = "#" Then
                p += 1
                co += 1
            ElseIf p <= Len(sourceText) And Mid(sourceText, p, 1) = "(" Then
                Dim bal As Long = 0
                While p <= Len(sourceText)
                    Dim c2 As String = Mid(sourceText, p, 1)
                    If c2 = "(" Then bal += 1
                    If c2 = ")" Then
                        bal -= 1
                        p += 1
                        co += 1
                        If bal = 0 Then Exit While
                        Continue While
                    End If
                    p += 1
                    co += 1
                Wend
                If bal <> 0 Then
                    g_uxsLexError = "Lexer hatasi: kapanmayan meta parantezi"
                    Exit Sub
                End If
            Else
                While p <= Len(sourceText) And UXS_IsDigit(Mid(sourceText, p, 1))
                    p += 1
                    co += 1
                Wend
            End If
            UXS_AddToken UXS_TOK_META, Mid(sourceText, startP, p - startP), ln, startC
            Continue While
        End If

        If ch = Chr(34) Then
            Dim closed As Long = 0
            p += 1
            co += 1
            While p <= Len(sourceText)
                Dim cs As String = Mid(sourceText, p, 1)
                If cs = Chr(92) And p < Len(sourceText) Then
                    p += 2
                    co += 2
                    Continue While
                End If
                If cs = Chr(34) Then
                    p += 1
                    co += 1
                    closed = -1
                    Exit While
                End If
                p += 1
                co += 1
            Wend
            If closed = 0 Then
                g_uxsLexError = "Lexer hatasi: kapanmayan string literal"
                Exit Sub
            End If
            UXS_AddToken UXS_TOK_STRING, Mid(sourceText, startP, p - startP), ln, startC
            Continue While
        End If

        If UXS_IsDigit(ch) Then
            While p <= Len(sourceText) And UXS_IsDigit(Mid(sourceText, p, 1))
                p += 1
                co += 1
            Wend
            UXS_AddToken UXS_TOK_NUMBER, Mid(sourceText, startP, p - startP), ln, startC
            Continue While
        End If

        If UXS_IsIdent(ch) Then
            While p <= Len(sourceText) And UXS_IsIdent(Mid(sourceText, p, 1))
                p += 1
                co += 1
            Wend
            UXS_AddToken UXS_TOK_IDENT, Mid(sourceText, startP, p - startP), ln, startC
            Continue While
        End If

        UXS_AddToken UXS_TOK_SYMBOL, ch, ln, startC
        p += 1
        co += 1
    Wend

    UXS_AddToken UXS_TOK_EOF, "", ln, co
End Sub

Function UXS_IsAstCommand(ByVal ch As String) As Long
    Return IIf(ch = ">" Or ch = "<" Or ch = "+" Or ch = "-" Or ch = "." Or ch = "," Or ch = "[" Or ch = "]", -1, 0)
End Function

Function UXS_ParseToUIR(ByRef nodeCount As Long, ByRef errText As String) As Long
    Dim i As Long
    Dim loopDepth As Long = 0
    nodeCount = 0
    errText = ""
    g_uxsLastStats.metaCount = 0
    g_uxsLastStats.stringCount = 0
    g_uxsLastStats.commandCount = 0

    For i = 1 To g_uxsTokenCount
        Select Case g_uxsTokens(i).kind
        Case UXS_TOK_META
            nodeCount += 1
            g_uxsLastStats.metaCount += 1
        Case UXS_TOK_STRING
            nodeCount += 1
            g_uxsLastStats.stringCount += 1
        Case UXS_TOK_SYMBOL
            Dim ch As String = g_uxsTokens(i).text
            If UXS_IsAstCommand(ch) Then
                nodeCount += 1
                g_uxsLastStats.commandCount += 1
                If ch = "[" Then loopDepth += 1
                If ch = "]" Then
                    loopDepth -= 1
                    If loopDepth < 0 Then
                        errText = "Parser hatasi: eslesmeyen kapanis ]"
                        Return 0
                    End If
                End If
            End If
        End Select
    Next i

    If loopDepth <> 0 Then
        errText = "Parser hatasi: eslesmeyen loop bloklari"
        Return 0
    End If
    Return -1
End Function

Function UXS_IsAddressableCommand(ByVal ch As String) As Long
    Select Case ch
    Case ">", "<", "+", "-", "0", ".", ",", "[", "]", "$", "%", "?", "!", ";", "&", "|", "^", "~", "{", "}", "e", "E"
        Return -1
    End Select
    Return 0
End Function

Function UXS_CollectAddressModes(ByVal sourceText As String, ByRef validCount As Long, ByRef invalidCount As Long, ByRef errText As String) As Long
    Dim i As Long = 1
    validCount = 0
    invalidCount = 0
    errText = ""

    While i <= Len(sourceText)
        Dim ch As String = Mid(sourceText, i, 1)
        If UXS_IsAddressableCommand(ch) Then
            If i < Len(sourceText) And Mid(sourceText, i + 1, 1) = "(" Then
                Dim j As Long = i + 1
                Dim bal As Long = 0
                While j <= Len(sourceText)
                    Dim cj As String = Mid(sourceText, j, 1)
                    If cj = "(" Then
                        bal += 1
                    ElseIf cj = ")" Then
                        bal -= 1
                        If bal = 0 Then Exit While
                    End If
                    j += 1
                Wend

                If bal <> 0 Then
                    invalidCount += 1
                    If errText = "" Then errText = "Adresleme parantezi kapatilmamis. Komut: " & ch
                    i += 1
                    Continue While
                End If

                Dim modeText As String = Mid(sourceText, i + 1, j - i)
                Dim parsed As UXMAddress
                If UXMParseAddressMode(modeText, parsed) Then
                    validCount += 1
                Else
                    invalidCount += 1
                    If errText = "" Then errText = "Gecersiz adresleme modu: " & modeText
                End If
                i = j + 1
                Continue While
            End If
        End If
        i += 1
    Wend

    Return IIf(invalidCount = 0, -1, 0)
End Function

Function UXS_FrontendLastError() As String
    Return g_uxsLastError
End Function

Function UXS_FrontendStatTokenCount() As Long
    Return g_uxsLastStats.tokenCount
End Function

Function UXS_FrontendStatNodeCount() As Long
    Return g_uxsLastStats.astNodeCount
End Function

Function UXS_FrontendStatAddressValidCount() As Long
    Return g_uxsLastStats.addressValidCount
End Function

Function UXS_FrontendStatAddressInvalidCount() As Long
    Return g_uxsLastStats.addressInvalidCount
End Function

Function UXS_FrontendStatMetaCount() As Long
    Return g_uxsLastStats.metaCount
End Function

Function UXS_FrontendStatStringCount() As Long
    Return g_uxsLastStats.stringCount
End Function

Function UXS_FrontendStatCommandCount() As Long
    Return g_uxsLastStats.commandCount
End Function

' Tek frontend kapisi: kaynak -> UIR
function UXS_FrontendBuildUIR(byval sourceText as String) as Long
    g_uxsLastError = ""
    g_uxsLastStats.tokenCount = 0
    g_uxsLastStats.astNodeCount = 0
    g_uxsLastStats.addressValidCount = 0
    g_uxsLastStats.addressInvalidCount = 0
    g_uxsLastStats.metaCount = 0
    g_uxsLastStats.stringCount = 0
    g_uxsLastStats.commandCount = 0

    if Len(sourceText)=0 then
        g_uxsLastError = "Kaynak bos oldugu icin frontend UIR uretemedi."
        return 0
    end if

    UXS_Lex sourceText
    If Len(g_uxsLexError) > 0 Then
        g_uxsLastError = g_uxsLexError
        Return 0
    End If
    g_uxsLastStats.tokenCount = g_uxsTokenCount
    If g_uxsTokenCount <= 0 Then
        g_uxsLastError = "Lexer token uretemedi."
        Return 0
    End If

    Dim nodeCount As Long = 0
    Dim parseErr As String
    If UXS_ParseToUIR(nodeCount, parseErr) = 0 Then
        g_uxsLastError = parseErr
        Return 0
    End If
    g_uxsLastStats.astNodeCount = nodeCount

    Dim addrErr As String
    If UXS_CollectAddressModes(sourceText, g_uxsLastStats.addressValidCount, g_uxsLastStats.addressInvalidCount, addrErr) = 0 Then
        g_uxsLastError = "Adresleme dogrulamasi basarisiz: " & addrErr
        Return 0
    End If

    return -1
end function

#endif
