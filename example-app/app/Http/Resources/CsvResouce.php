<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Str;

class CsvResouce extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request)
    {
        //return parent::toArray($request);

        //começar api sem paginação !
        return [

            'NM_CANDIDATO' => $this->NM_CANDIDATO,
            'NM_URNA_CANDIDATO' => $this->NM_URNA_CANDIDATO,
            'NR_CPF_CANDIDATO' => $this->when(Str::length($this->NR_CPF_CANDIDATO) < 11,function(){
                return '0'.$this->NR_CPF_CANDIDATO;
            },$this->NR_CPF_CANDIDATO),
            'SG_UF' => $this->SG_UF,
            'NM_UE' => $this->NM_UE,
            'DS_CARGO' => $this->DS_CARGO,
            'ANO_ELEICAO' => $this->ANO_ELEICAO,
            'NR_CANDIDATO' => $this->NR_CANDIDATO,
            'CD_ELEICAO' => $this->CD_ELEICAO,

            'bairro2018' => $this->when($request->get('bairro') === 'bairro2018',function() use($request){
                if($request->get('UF') and $request->get('bairro') === 'bairro2018'){
                    return $this->bairro2018()->where("NM_MUNICIPIO", request()->get('UF'))->get();//->paginate(10);
                }
                return $this->bairro2018()->get();//paginate(10);
            }),

        ];
    }
}
