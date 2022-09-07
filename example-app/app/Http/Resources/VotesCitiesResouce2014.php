<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class VotesCitiesResouce2014 extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array|\Illuminate\Contracts\Support\Arrayable|\JsonSerializable
     */
    public function toArray($request)
    {
        return[
            'NM_VOTAVEL' => $this->NM_VOTAVEL,
            'NR_VOTAVEL' => $this->NR_VOTAVEL,
            'DT_GERACAO_HH_GERACAO' => $this->DT_GERACAO_HH_GERACAO,
            'DS_CARGO_PERGUNTA' => $this->DS_CARGO_PERGUNTA,
            'NM_MUNICIPIO' => $this->NM_MUNICIPIO,
            'QT_VOTOS' => $this->QT_VOTOS,
        ];
        //return parent::toArray($request);
    }
}
